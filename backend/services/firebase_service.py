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
        
        self.db = None
        self.students_collection = None
        self.opportunities_collection = None
        self.reasoning_collection = None
        self.firebase_enabled = False
        
        try:
            # Initialize Firebase
            if not firebase_admin._apps:
                self._initialize_firebase()
            
            # Get Firestore client
            self.db = firestore.client()
            
            # Collection references
            self.students_collection = self.db.collection('students')
            self.opportunities_collection = self.db.collection('opportunities')
            self.reasoning_collection = self.db.collection('reasoning_results')
            
            self.firebase_enabled = True
            print("✅ Firebase initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("⚠️  Application will continue with limited functionality")
            self.firebase_enabled = False
    
    def _initialize_firebase(self):
        """Initialize Firebase instance with credentials"""
        # Priority 1: Try new credentials file (firebase-credentials-2.json)
        if os.path.exists('./firebase-credentials-2.json'):
            print("✓ Initializing Firebase with: firebase-credentials-2.json")
            cred = credentials.Certificate('./firebase-credentials-2.json')
            firebase_admin.initialize_app(cred)
            return
        
        # Priority 2: Try environment variable with JSON string
        firebase_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        if firebase_json:
            print("✓ Initializing Firebase from FIREBASE_CREDENTIALS_JSON")
            try:
                config_dict = json.loads(firebase_json)
                cred = credentials.Certificate(config_dict)
                firebase_admin.initialize_app(cred)
                return
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse FIREBASE_CREDENTIALS_JSON: {e}")
                raise
        
        # Priority 3: Try file path from environment variable
        elif os.getenv('FIREBASE_CONFIG_PATH'):
            firebase_config_path = os.getenv('FIREBASE_CONFIG_PATH')
            if os.path.exists(firebase_config_path):
                print(f"✓ Initializing Firebase: {firebase_config_path}")
                cred = credentials.Certificate(firebase_config_path)
                firebase_admin.initialize_app(cred)
                return
            else:
                raise FileNotFoundError(f"Firebase credentials file not found: {firebase_config_path}")
        
        # Priority 4: Try old default file location (for backward compatibility)
        elif os.path.exists('./firebase-credentials.json'):
            print("✓ Initializing Firebase with: firebase-credentials.json")
            cred = credentials.Certificate('./firebase-credentials.json')
            firebase_admin.initialize_app(cred)
            return
        
        # No credentials found
        else:
            print("❌ ERROR: No Firebase credentials provided!")
            raise ValueError("Firebase credentials not configured")
    
    
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
    
    
    # ========================================================================
    # APPLICATION TRACKER OPERATIONS
    # ========================================================================
    
    def create_application(self, user_id, application_data):
        """Create new application tracking entry"""
        if not self.firebase_enabled:
            print("⚠️  Firebase disabled - cannot create application")
            return {'id': 'unsaved', **application_data}
        
        try:
            from datetime import datetime
            
            application_ref = self.db.collection('applications').document()
            
            # Create a copy to avoid modifying original
            app_data_to_save = application_data.copy()
            app_data_to_save.update({
                'user_id': user_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            application_ref.set(app_data_to_save)
            print(f"✓ Created application {application_ref.id}")
            
            # Return JSON-serializable data (replace SERVER_TIMESTAMP with current time)
            return {
                'id': application_ref.id,
                'user_id': user_id,
                'opportunity_title': application_data.get('opportunity_title'),
                'opportunity_link': application_data.get('opportunity_link'),
                'deadline': application_data.get('deadline'),
                'status': application_data.get('status'),
                'priority': application_data.get('priority'),
                'notes': application_data.get('notes', ''),
                'eligibility_score': application_data.get('eligibility_score'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error creating application: {str(e)}")
            raise
    
    
    def get_user_applications(self, user_id):
        """Get all applications for a user"""
        if not self.firebase_enabled:
            print("⚠️  Firebase disabled - cannot retrieve applications")
            return []
        
        try:
            applications = []
            docs = self.db.collection('applications')\
                .where(filter=firestore.FieldFilter('user_id', '==', user_id))\
                .stream()
            
            for doc in docs:
                app_data = doc.to_dict()
                app_data['id'] = doc.id
                
                # Convert Firestore timestamps to ISO strings for JSON serialization
                if 'created_at' in app_data and app_data['created_at']:
                    try:
                        # Check if it's already a string
                        if not isinstance(app_data['created_at'], str):
                            app_data['created_at'] = app_data['created_at'].isoformat()
                    except Exception as e:
                        print(f"Warning: Could not convert created_at: {e}")
                        app_data['created_at'] = None
                        
                if 'updated_at' in app_data and app_data['updated_at']:
                    try:
                        # Check if it's already a string
                        if not isinstance(app_data['updated_at'], str):
                            app_data['updated_at'] = app_data['updated_at'].isoformat()
                    except Exception as e:
                        print(f"Warning: Could not convert updated_at: {e}")
                        app_data['updated_at'] = None
                        
                applications.append(app_data)
            
            # Sort by created_at in Python (descending - newest first)
            # Use empty string as default for None values to avoid comparison errors
            try:
                applications.sort(key=lambda x: str(x.get('created_at') or ''), reverse=True)
            except Exception as sort_error:
                print(f"Warning: Sort failed: {sort_error}. Returning unsorted applications")
                # Print debug info
                for app in applications:
                    print(f"  App ID {app.get('id')}: created_at = {app.get('created_at')} (type: {type(app.get('created_at'))})")
            
            print(f"✓ Retrieved {len(applications)} applications for user {user_id}")
            return applications
        except Exception as e:
            print(f"❌ Error fetching applications: {str(e)}")
            raise
    
    
    def update_application_status(self, application_id, status, notes=None):
        """Update application status"""
        if not self.firebase_enabled:
            print("⚠️  Firebase disabled - cannot update application")
            return {'success': False}
        
        try:
            from datetime import datetime
            
            update_data = {
                'status': status,
                'updated_at': firestore.SERVER_TIMESTAMP
            }
            if notes:
                update_data['notes'] = notes
                
            self.db.collection('applications').document(application_id).update(update_data)
            print(f"✓ Updated application {application_id} status to {status}")
            
            # Return JSON-safe response
            return {
                'success': True, 
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error updating application: {str(e)}")
            raise
