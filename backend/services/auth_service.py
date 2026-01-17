"""
Authentication Service
Handles user registration, login, and session management
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from firebase_admin import firestore

# In-memory session store (use Redis in production)
active_sessions = {}

def hash_password(password):
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def register_user(email, password, name):
    """
    Register new user
    Returns: user_id and session_token on success, None on failure
    """
    db = firestore.client()
    users_ref = db.collection('users')
    
    # Check if user already exists
    existing = users_ref.where('email', '==', email).limit(1).get()
    if len(list(existing)) > 0:
        raise ValueError('User with this email already exists')
    
    # Create new user
    user_data = {
        'email': email,
        'password_hash': hash_password(password),
        'name': name,
        'created_at': datetime.utcnow().isoformat(),
        'profile_id': None  # Will be set when they upload resume
    }
    
    user_ref = users_ref.add(user_data)
    user_id = user_ref[1].id
    
    # Create session
    session_token = generate_session_token()
    active_sessions[session_token] = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'expires_at': datetime.utcnow() + timedelta(days=7)
    }
    
    return {
        'user_id': user_id,
        'email': email,
        'name': name,
        'session_token': session_token
    }

def login_user(email, password):
    """
    Login existing user with optimized Firestore queries
    Returns: user data and session_token on success
    Raises: ValueError on invalid credentials or errors
    """
    if not email or not password:
        raise ValueError('Email and password are required')
    
    try:
        db = firestore.client()
        
        # FAST METHOD: Get all users and filter in memory (better than slow Firestore query)
        users_ref = db.collection('users')
        
        # Get specific user by ID if we know the pattern, otherwise scan
        # For jayanarayanmenon@gmail.com, we know the ID is 8eD238uK7YyqP2wzn0P7
        KNOWN_USERS = {
            'jayanarayanmenon@gmail.com': '8eD238uK7YyqP2wzn0P7'
        }
        
        user_doc = None
        user_data = None
        user_id = None
        
        # Try direct lookup first for known users
        if email in KNOWN_USERS:
            user_id = KNOWN_USERS[email]
            user_doc_ref = users_ref.document(user_id)
            user_doc_data = user_doc_ref.get()
            if user_doc_data.exists:
                user_data = user_doc_data.to_dict()
                if user_data.get('email') == email:
                    user_doc = user_doc_data
        
        # If not found, scan collection (slower but works for all users)
        if not user_doc:
            all_users = users_ref.stream()
            for doc in all_users:
                doc_data = doc.to_dict()
                if doc_data.get('email') == email:
                    user_doc = doc
                    user_data = doc_data
                    user_id = doc.id
                    break
        
        if not user_doc or not user_data:
            raise ValueError('Invalid email or password')
        
        # Verify password
        password_hash = hash_password(password)
        if user_data.get('password_hash') != password_hash:
            raise ValueError('Invalid email or password')
        
        # Create session token
        session_token = generate_session_token()
        session_data = {
            'user_id': user_id,
            'email': user_data['email'],
            'name': user_data.get('name', email.split('@')[0]),
            'profile_id': user_data.get('profile_id'),
            'expires_at': datetime.utcnow() + timedelta(days=7)
        }
        active_sessions[session_token] = session_data
        
        print(f"✅ Login successful: {email}")
        
        # Return user data with session
        return {
            'user_id': user_id,
            'email': user_data['email'],
            'name': session_data['name'],
            'profile_id': user_data.get('profile_id'),
            'session_token': session_token
        }
        
    except ValueError:
        raise
    except Exception as e:
        print(f"❌ Login error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise ValueError('Unable to connect to authentication service')

def verify_session(session_token):
    """
    Verify session token is valid
    Returns: user data if valid, None if invalid
    """
    if not session_token or session_token not in active_sessions:
        return None
    
    session = active_sessions[session_token]
    
    # Check expiration
    if datetime.utcnow() > session['expires_at']:
        del active_sessions[session_token]
        return None
    
    return session

def logout_user(session_token):
    """Logout user by removing session"""
    if session_token in active_sessions:
        del active_sessions[session_token]
    return True

def link_profile_to_user(user_id, profile_id):
    """Link a profile to a user account"""
    db = firestore.client()
    users_ref = db.collection('users')
    
    user_ref = users_ref.document(user_id)
    user_ref.update({
        'profile_id': profile_id,
        'profile_linked_at': datetime.utcnow().isoformat()
    })
    
    # Update all active sessions for this user
    for token, session in active_sessions.items():
        if session['user_id'] == user_id:
            session['profile_id'] = profile_id
    
    return True

def get_user_profile(user_id):
    """Get user's linked profile ID"""
    db = firestore.client()
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    
    if not user_doc.exists:
        return None
    
    user_data = user_doc.to_dict()
    return user_data.get('profile_id')
