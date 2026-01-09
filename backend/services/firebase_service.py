"""
Firebase Service - Handles all Firebase Firestore operations with comprehensive error handling
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime


class FirebaseService:
    def __init__(self):
        """Initialize Firebase Admin SDK with comprehensive error handling"""
        
        self.db = None
        self.students_collection = None
        self.opportunities_collection = None
        self.reasoning_collection = None
        self.firebase_enabled = False
        
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                # Try to get Firebase config from environment
                firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH')
                
                if firebase_config_path and os.path.exists(firebase_config_path):
                    # Use service account file
                    print(f"✓ Initializing Firebase with config file: {firebase_config_path}")
                    cred = credentials.Certificate(firebase_config_path)
                    firebase_admin.initialize_app(cred)
                elif os.getenv('FIREBASE_CONFIG_JSON'):
                    # Use JSON string from environment
                    print("✓ Initializing Firebase with JSON config")
                    config_dict = json.loads(os.getenv('FIREBASE_CONFIG_JSON'))
                    cred = credentials.Certificate(config_dict)
                    firebase_admin.initialize_app(cred)
                else:
                    # Use default credentials (for local development/testing)
                    print("⚠️  Warning: No Firebase credentials provided.")
                    print("⚠️  Firebase operations will be disabled. System will still function with in-memory storage.")
                    firebase_admin.initialize_app()
            
            # Get Firestore client
            self.db = firestore.client()
            
            # Collection references
            self.students_collection = self.db.collection('students')
            self.opportunities_collection = self.db.collection('opportunities')
            self.reasoning_collection = self.db.collection('reasoning_results')
            
            self.firebase_enabled = True
            print("✓ Firebase initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("⚠️  Application will continue with limited functionality")
            self.firebase_enabled = False
    
    
    # ========================================================================
    # STUDENT PROFILE OPERATIONS
    # ========================================================================
    
    def create_student_profile(self, profile_data, resume_text=None):
        """
        Create a new student profile in Firestore
        
        Args:
            profile_data: Structured profile dictionary
            resume_text: Optional raw resume text
        
        Returns:
            Dictionary with profile_id and profile_data
        """
        if not self.firebase_enabled:
            print("⚠️  Firebase disabled - generating mock profile ID")
            return {
                'profile_id': f"mock_{datetime.now().timestamp()}",
                'profile_data': profile_data
            }
        
        try:
            doc_ref = self.students_collection.document()
            
            student = {
                'profile': profile_data,
                'resume_text': resume_text,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref.set(student)
            
            return {
                'profile_id': doc_ref.id,
                'profile_data': profile_data
            }
        except Exception as e:
            print(f"❌ Error creating profile: {e}")
            return {
                'profile_id': f"error_{datetime.now().timestamp()}",
                'profile_data': profile_data
            }
    
    
    def get_student_profile(self, profile_id):
        """
        Get student profile by ID
        
        Returns:
            Profile dictionary or None
        """
        if not self.firebase_enabled:
            print(f"⚠️  Firebase disabled - cannot retrieve profile {profile_id}")
            return None
        
        try:
            doc_ref = self.students_collection.document(profile_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['profile_id'] = doc.id
                print(f"✓ Retrieved profile {profile_id}")
                return data
            else:
                print(f"⚠️  Profile {profile_id} not found")
                return None
                
        except Exception as e:
            print(f"❌ Error getting profile {profile_id}: {e}")
            return None
    
    
    def update_student_profile(self, profile_id, profile_data):
        """Update existing student profile"""
        if not self.firebase_enabled:
            return {'success': False, 'error': 'Firebase disabled'}
        
        try:
            doc_ref = self.students_collection.document(profile_id)
            doc_ref.update({
                'profile': profile_data,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            return {'success': True, 'profile_id': profile_id}
        except Exception as e:
            print(f"❌ Error updating profile: {e}")
            return {'success': False, 'error': str(e)}
    
    
    # ========================================================================
    # OPPORTUNITY OPERATIONS
    # ========================================================================
    
    def create_opportunity(self, opportunity_data):
        """Create or update an opportunity (cache it)"""
        if not self.firebase_enabled:
            mock_id = f"opp_{datetime.now().timestamp()}"
            return {'opportunity_id': mock_id, **opportunity_data}
        
        try:
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
        except Exception as e:
            print(f"❌ Error creating opportunity: {e}")
            mock_id = f"error_{datetime.now().timestamp()}"
            return {'opportunity_id': mock_id, **opportunity_data}
    
    
    def get_opportunity(self, opportunity_id):
        """Get opportunity by ID"""
        if not self.firebase_enabled:
            print(f"⚠️  Firebase disabled - cannot retrieve opportunity {opportunity_id}")
            return None
        
        try:
            doc_ref = self.opportunities_collection.document(opportunity_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['opportunity_id'] = doc.id
                print(f"✓ Retrieved opportunity {opportunity_id}")
                return data
            else:
                print(f"⚠️  Opportunity {opportunity_id} not found")
                return None
                
        except Exception as e:
            print(f"❌ Error getting opportunity {opportunity_id}: {e}")
            return None
    
    
    # ========================================================================
    # REASONING RESULTS OPERATIONS
    # ========================================================================
    
    def create_reasoning_result(self, profile_id, opportunity_id, analysis):
        """Store reasoning result - ALWAYS returns result even if Firebase fails"""
        if not self.firebase_enabled:
            print("⚠️  Firebase disabled - returning analysis without saving")
            return {
                'reasoning_id': 'unsaved',
                **analysis
            }
        
        try:
            doc_ref = self.reasoning_collection.document()
            
            reasoning = {
                'profile_id': profile_id,
                'opportunity_id': opportunity_id,
                'analysis': analysis,
                'analyzed_at': firestore.SERVER_TIMESTAMP
            }
            
            doc_ref.set(reasoning)
            
            print(f"✓ Saved reasoning result {doc_ref.id}")
            return {
                'reasoning_id': doc_ref.id,
                **analysis
            }
            
        except Exception as e:
            print(f"❌ Error saving reasoning result: {e}")
            # CRITICAL: Return analysis even if save fails
            return {
                'reasoning_id': 'error',
                **analysis
            }
    
    
    def get_cached_reasoning(self, profile_id, opportunity_id):
        """Check if reasoning already exists"""
        if not self.firebase_enabled:
            return None
        
        try:
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
            
        except Exception as e:
            print(f"❌ Error getting cached reasoning: {e}")
            return None
