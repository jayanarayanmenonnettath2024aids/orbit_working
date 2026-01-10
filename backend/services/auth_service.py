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
    Login existing user
    Returns: user data and session_token on success, None on failure
    """
    db = firestore.client()
    users_ref = db.collection('users')
    
    # Find user by email
    users = users_ref.where('email', '==', email).limit(1).get()
    users_list = list(users)
    
    if len(users_list) == 0:
        raise ValueError('Invalid email or password')
    
    user_doc = users_list[0]
    user_data = user_doc.to_dict()
    
    # Verify password
    password_hash = hash_password(password)
    if user_data['password_hash'] != password_hash:
        raise ValueError('Invalid email or password')
    
    # Create session
    session_token = generate_session_token()
    active_sessions[session_token] = {
        'user_id': user_doc.id,
        'email': user_data['email'],
        'name': user_data.get('name', email.split('@')[0]),
        'profile_id': user_data.get('profile_id'),
        'expires_at': datetime.utcnow() + timedelta(days=7)
    }
    
    return {
        'user_id': user_doc.id,
        'email': user_data['email'],
        'name': user_data.get('name', email.split('@')[0]),
        'profile_id': user_data.get('profile_id'),
        'session_token': session_token
    }

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
