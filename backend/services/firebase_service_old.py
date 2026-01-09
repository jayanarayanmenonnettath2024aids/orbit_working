"""
Firebase Service - Handles all Firebase Firestore operations
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime


class FirebaseService:
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                # Try to get Firebase config from environment
                firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH')
                
                if firebase_config_path and os.path.exists(firebase_config_path):
                    # Use service account file
                    print(f"Initializing Firebase with config file: {firebase_config_path}")
                    cred = credentials.Certificate(firebase_config_path)
                    firebase_admin.initialize_app(cred)
                elif os.getenv('FIREBASE_CONFIG_JSON'):
                    # Use JSON string from environment
                    print("Initializing Firebase with JSON config")
                    config_dict = json.loads(os.getenv('FIREBASE_CONFIG_JSON'))
                    cred = credentials.Certificate(config_dict)
                    firebase_admin.initialize_app(cred)
                else:
                    # Use default credentials (for local development/testing)
                    print("⚠️  Warning: No Firebase credentials provided. Using default credentials.")
                    print("⚠️  Firebase operations may fail without proper configuration.")
                    firebase_admin.initialize_app()
            
            # Get Firestore client
            self.db = firestore.client()
            
            # Collection references
            self.students_collection = self.db.collection('students')
            self.opportunities_collection = self.db.collection('opportunities')
            self.reasoning_collection = self.db.collection('reasoning_results')
            
            print("✓ Firebase initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("⚠️  Application will continue but database operations will fail")
            self.db = None
            self.students_collection = None
            self.opportunities_collection = None
            self.reasoning_collection = None
    
    
    # ========================================================================
    # STUDENT PROFILE OPERATIONS
    # ========================================================================
    
    def create_student_profile(self, profile_data, resume_text=None):
        """
        Create a new student profile
        
        Args:
            profile_data: Dictionary with structured profile
            resume_text: Optional raw resume text
        
        Returns:
            Dictionary with profile_id and created profile
        """
        doc_ref = self.students_collection.document()
        
        profile = {
            'profile': profile_data,
            'resume_text': resume_text or '',
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        doc_ref.set(profile)
        
        return {
            'profile_id': doc_ref.id,
            'profile_data': profile_data
        }
    
    
    def get_student_profile(self, profile_id):
        """
        Get student profile by ID
        
        Returns:
            Profile dictionary or None
        """
        try:
            if not self.students_collection:
                print("❌ Firebase not initialized - cannot get profile")
                return None
                
            doc_ref = self.students_collection.document(profile_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['profile_id'] = doc.id
                return data
            
            print(f"⚠️  Profile {profile_id} not found in Firebase")
            return None
            
        except Exception as e:
            print(f"❌ Error getting profile {profile_id}: {e}")
            return None
    
    
    def update_student_profile(self, profile_id, profile_data):
        """
        Update existing student profile
        """
        doc_ref = self.students_collection.document(profile_id)
        doc_ref.update({
            'profile': profile_data,
            'updated_at': firestore.SERVER_TIMESTAMP
        })
        
        return {'success': True, 'profile_id': profile_id}
    
    
    # ========================================================================
    # OPPORTUNITY OPERATIONS
    # ========================================================================
    
    def create_opportunity(self, opportunity_data):
        """
        Create or update an opportunity (cache it)
        
        Args:
            opportunity_data: Dictionary with opportunity details
        
        Returns:
            Dictionary with opportunity_id
        """
        doc_ref = self.opportunities_collection.document()
        
        opportunity = {
            **opportunity_data,
            'cached_at': firestore.SERVER_TIMESTAMP
        }
        
        doc_ref.set(opportunity)
        
        return {
            'opportunity_id': doc_ref.id,
            **opportunity_data
        }
    
    
    def get_opportunity(self, opportunity_id):
        """
        Get opportunity by ID
        
        Returns:
            Opportunity dictionary or None
        """
        try:
            if not self.opportunities_collection:
                print("❌ Firebase not initialized - cannot get opportunity")
                return None
                
            doc_ref = self.opportunities_collection.document(opportunity_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['opportunity_id'] = doc.id
                return data
            
            print(f"⚠️  Opportunity {opportunity_id} not found in Firebase")
            return None
            
        except Exception as e:
            print(f"❌ Error getting opportunity {opportunity_id}: {e}")
            return None
    
    
    def get_cached_opportunities(self, limit=20, opportunity_type=None):
        """
        Get recently cached opportunities
        
        Args:
            limit: Max number of results
            opportunity_type: Filter by type
        
        Returns:
            List of opportunities
        """
        query = self.opportunities_collection.order_by(
            'cached_at', direction=firestore.Query.DESCENDING
        ).limit(limit)
        
        if opportunity_type:
            query = query.where('type', '==', opportunity_type)
        
        docs = query.stream()
        
        opportunities = []
        for doc in docs:
            data = doc.to_dict()
            data['opportunity_id'] = doc.id
            opportunities.append(data)
        
        return opportunities
    
    
    def search_opportunities_by_title(self, search_term):
        """
        Search opportunities by title (basic text search)
        Note: Firestore doesn't support full-text search natively
        For production, consider using Algolia or Elasticsearch
        """
        docs = self.opportunities_collection.stream()
        
        results = []
        search_lower = search_term.lower()
        
        for doc in docs:
            data = doc.to_dict()
            title = data.get('title', '').lower()
            
            if search_lower in title:
                data['opportunity_id'] = doc.id
                results.append(data)
        
        return results
    
    
    # ========================================================================
    # REASONING RESULTS OPERATIONS
    # ========================================================================
    
    def create_reasoning_result(self, profile_id, opportunity_id, analysis):
        """
        Store reasoning result
        
        Args:
            profile_id: Student profile ID
            opportunity_id: Opportunity ID
            analysis: Gemini analysis result (dict)
        
        Returns:
            Dictionary with reasoning_id
        """
        try:
            if not self.reasoning_collection:
                print("⚠️  Firebase not initialized - returning analysis without saving")
                return {
                    'reasoning_id': 'unsaved',
                    **analysis
                }
            
            doc_ref = self.reasoning_collection.document()
            
            reasoning = {
                'profile_id': profile_id,
                'opportunity_id': opportunity_id,
                'analysis': analysis,
                'analyzed_at': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref.set(reasoning)
            
            return {
                'reasoning_id': doc_ref.id,
                **analysis
            }
            
        except Exception as e:
            print(f"❌ Error saving reasoning result: {e}")
            # Return analysis even if save fails
            return {
                'reasoning_id': 'error',
                **analysis
            }
    
    
    def get_reasoning_result(self, reasoning_id):
        """
        Get reasoning result by ID
        """
        doc_ref = self.reasoning_collection.document(reasoning_id)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            data['reasoning_id'] = doc.id
            return data
        
        return None
    
    
    def get_cached_reasoning(self, profile_id, opportunity_id):
        """
        Check if reasoning already exists for this profile + opportunity pair
        
        Returns:
            Cached reasoning or None
        """
        query = self.reasoning_collection \
            .where(filter=firestore.FieldFilter('profile_id', '==', profile_id)) \
            .where(filter=firestore.FieldFilter('opportunity_id', '==', opportunity_id)) \
            .order_by('analyzed_at', direction=firestore.Query.DESCENDING) \
            .limit(1)
        
        docs = list(query.stream())
        
        if docs:
            data = docs[0].to_dict()
            data['reasoning_id'] = docs[0].id
            return data
        
        return None
    
    
    def get_reasoning_by_profile(self, profile_id, limit=10):
        """
        Get all reasoning results for a profile
        """
        query = self.reasoning_collection \
            .where('profile_id', '==', profile_id) \
            .order_by('analyzed_at', direction=firestore.Query.DESCENDING) \
            .limit(limit)
        
        docs = query.stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['reasoning_id'] = doc.id
            results.append(data)
        
        return results
    
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def batch_get(self, collection_name, doc_ids):
        """
        Get multiple documents at once
        """
        collection = self.db.collection(collection_name)
        docs = []
        
        for doc_id in doc_ids:
            doc = collection.document(doc_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                docs.append(data)
        
        return docs
    
    
    def delete_document(self, collection_name, doc_id):
        """
        Delete a document (for cleanup/testing)
        """
        self.db.collection(collection_name).document(doc_id).delete()
        return {'success': True}
