"""
Main Flask application for AI-Powered Opportunity Intelligence System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import traceback
from dotenv import load_dotenv

# Import services
from services.profile_service import ProfileService
from services.opportunity_service import OpportunityService
from services.reasoning_service import ReasoningService
from services.firebase_service import FirebaseService
from services.chatbot_service import ChatbotService
from services.gamification_service import GamificationService
from services.analytics_service import AnalyticsService
from services.success_stories_service import SuccessStoriesService
from services.auth_service import (
    register_user, 
    login_user, 
    verify_session, 
    logout_user,
    link_profile_to_user,
    get_user_profile
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS properly for development
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=False)

# Initialize services
firebase_service = FirebaseService()
profile_service = ProfileService(firebase_service)
opportunity_service = OpportunityService(firebase_service)
reasoning_service = ReasoningService(firebase_service)
chatbot_service = ChatbotService()
gamification_service = GamificationService(firebase_service)
analytics_service = AnalyticsService(firebase_service)
success_stories_service = SuccessStoriesService(firebase_service)

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register new user
    
    Expected: { email, password, name }
    Returns: { user_id, email, name, session_token }
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        result = register_user(email, password, name)
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"❌ Registration error: {e}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    """
    User login endpoint
    POST { email, password } → { user_id, email, name, profile_id, session_token }
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Attempt login
        result = login_user(email, password)
        return jsonify(result), 200
        
    except ValueError as e:
        # Invalid credentials or validation error
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        # Unexpected server error
        print(f"❌ Login error: {type(e).__name__}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/logout', methods=['POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])
def logout():
    """
    Logout user
    
    Expected: { session_token }
    Returns: { success: true }
    """
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
            
        session_token = data.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Session token required'}), 400
        
        logout_user(session_token)
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify():
    """
    Verify session token
    
    Expected: { session_token }
    Returns: { valid: true, user: {...} } or { valid: false }
    """
    try:
        data = request.json
        session_token = data.get('session_token')
        
        session = verify_session(session_token)
        
        if session:
            return jsonify({
                'valid': True,
                'user': {
                    'user_id': session['user_id'],
                    'email': session['email'],
                    'name': session['name'],
                    'profile_id': session.get('profile_id')
                }
            }), 200
        else:
            return jsonify({'valid': False}), 401
            
    except Exception as e:
        print(f"❌ Verify error: {e}")
        return jsonify({'valid': False}), 401

# ============================================================================
# PROFILE ENDPOINTS
# ============================================================================

@app.route('/api/profile/parse_resume', methods=['POST'])
def parse_resume():
    """
    Parse resume PDF and create/update profile for authenticated user
    
    Expected: multipart/form-data with 'resume' file
    Headers: Authorization: Bearer <session_token>
    Returns: { profile_id, profile_data }
    """
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization', '')
        session_token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None
        
        session = verify_session(session_token)
        if not session:
            return jsonify({'error': 'Unauthorized. Please login.'}), 401
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if user already has a profile
        existing_profile_id = session.get('profile_id')
        
        if existing_profile_id:
            # Update existing profile
            print(f"🔄 Updating existing profile {existing_profile_id} for user {session['user_id']}")
            result = profile_service.parse_and_create_profile(resume_file)
            # Link the new profile to user
            link_profile_to_user(session['user_id'], result['profile_id'])
        else:
            # Create new profile
            print(f"✨ Creating new profile for user {session['user_id']}")
            result = profile_service.parse_and_create_profile(resume_file)
            # Link profile to user
            link_profile_to_user(session['user_id'], result['profile_id'])
        
        return jsonify(result), 201
        
    except Exception as e:
        print(f"❌ Parse resume error: {e}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Failed to parse resume: {str(e)}'}), 500


@app.route('/api/profile/create', methods=['POST'])
def create_profile():
    """
    Create profile from manual input
    
    Expected JSON:
    {
        "education": {...},
        "skills": {...},
        "experience": [...],
        "interests": [...],
        "self_description": "..."
    }
    
    Returns: { profile_id, profile_data }
    """
    try:
        profile_data = request.json
        
        if not profile_data:
            return jsonify({'error': 'No profile data provided'}), 400
        
        result = profile_service.create_profile_manual(profile_data)
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profile/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    """
    Get profile by ID
    
    Returns: { profile_id, profile_data, created_at }
    """
    try:
        profile = profile_service.get_profile(profile_id)
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify(profile), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# OPPORTUNITY ENDPOINTS
# ============================================================================

@app.route('/api/opportunities/search', methods=['POST'])
def search_opportunities():
    """
    Search for opportunities with filters and pagination
    
    Expected JSON:
    {
        "query": "AI hackathon India",
        "opportunity_type": "hackathon",  // optional: filter by type
        "year": "2026",  // optional: filter by year
        "page": 1,  // optional: pagination (default 1)
        "per_page": 10,  // optional: results per page (default 10)
        "force_refresh": false  // optional: skip cache and force new search
    }
    
    Returns: { opportunities: [...], count, total, page, has_more }
    """
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query required'}), 400
        
        query = data['query']
        opportunity_type = data.get('opportunity_type', None)
        year_filter = data.get('year', None)
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)
        force_refresh = data.get('force_refresh', False)
        
        # Log if force refresh requested
        if force_refresh:
            print("🔄 Force refresh requested - bypassing cache")
        
        # Search opportunities
        result = opportunity_service.search_opportunities(query, opportunity_type)
        all_opportunities = result['opportunities']
        
        # Award points for search (if user_id provided)
        user_id = data.get('user_id')
        if user_id:
            try:
                gamification_service.award_points(user_id, 'search_opportunity')
            except:
                pass  # Don't fail request if gamification fails
        
        # Apply year filter if specified
        if year_filter:
            all_opportunities = [
                opp for opp in all_opportunities 
                if opp.get('year') == year_filter
            ]
        
        # Calculate pagination
        total = len(all_opportunities)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_opportunities = all_opportunities[start_idx:end_idx]
        
        return jsonify({
            'opportunities': paginated_opportunities,
            'count': len(paginated_opportunities),
            'total': total,
            'page': page,
            'per_page': per_page,
            'has_more': end_idx < total,
            'query': result['query']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/opportunities/suggestions/<profile_id>', methods=['GET'])
def get_personalized_suggestions(profile_id):
    """
    Get personalized search suggestions based on profile
    
    Returns: { suggestions: [...] }
    """
    try:
        # Get profile
        profile = profile_service.get_profile(profile_id)
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Generate suggestions
        suggestions = opportunity_service.generate_personalized_suggestions(profile['profile'])
        
        return jsonify({'suggestions': suggestions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/opportunities/cached', methods=['GET'])
def get_cached_opportunities():
    """
    Get recently cached opportunities
    
    Query params:
    - limit: number of results (default 20)
    - type: filter by type
    
    Returns: { opportunities: [...], count }
    """
    try:
        limit = int(request.args.get('limit', 20))
        opportunity_type = request.args.get('type', None)
        
        result = opportunity_service.get_cached_opportunities(limit, opportunity_type)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/opportunities/<opportunity_id>', methods=['GET'])
def get_opportunity(opportunity_id):
    """
    Get specific opportunity by ID
    
    Returns: opportunity object
    """
    try:
        opportunity = opportunity_service.get_opportunity(opportunity_id)
        
        if not opportunity:
            return jsonify({'error': 'Opportunity not found'}), 404
        
        return jsonify(opportunity), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# REASONING ENDPOINTS (CORE INTELLIGENCE)
# ============================================================================

@app.route('/api/reasoning/analyze', methods=['POST'])
def analyze_eligibility():
    """
    Analyze student eligibility for an opportunity using Gemini AI
    
    Expected JSON:
    {
        "profile_id": "uuid",
        "opportunity_id": "uuid"
    }
    
    Returns: {
        "reasoning_id": "uuid",
        "eligibility_status": "...",
        "reasons_met": [...],
        "reasons_not_met": [...],
        "missing_skills": [...],
        "missing_experience": [...],
        "confidence_score": 85,
        "explanation_simple": "...",
        "next_steps": [...]
    }
    """
    try:
        data = request.json
        
        if not data or 'profile_id' not in data or 'opportunity_id' not in data:
            return jsonify({'error': 'profile_id and opportunity_id required'}), 400
        
        profile_id = data['profile_id']
        opportunity_id = data['opportunity_id']
        
        # Check if already analyzed (cached)
        cached_result = reasoning_service.get_cached_reasoning(profile_id, opportunity_id)
        if cached_result:
            return jsonify({**cached_result, 'cached': True}), 200
        
        # Perform analysis
        result = reasoning_service.analyze_eligibility(profile_id, opportunity_id)
        
        return jsonify({**result, 'cached': False}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reasoning/batch', methods=['POST'])
def analyze_batch():
    """
    Analyze eligibility for multiple opportunities at once
    
    Expected JSON:
    {
        "profile_id": "uuid",
        "opportunity_ids": ["uuid1", "uuid2", ...]
    }
    
    Returns: {
        "results": [
            { "opportunity_id": "...", "analysis": {...} },
            ...
        ]
    }
    """
    try:
        data = request.json
        
        if not data or 'profile_id' not in data or 'opportunity_ids' not in data:
            return jsonify({'error': 'profile_id and opportunity_ids required'}), 400
        
        profile_id = data['profile_id']
        opportunity_ids = data['opportunity_ids']
        
        results = reasoning_service.analyze_batch(profile_id, opportunity_ids)
        
        return jsonify({'results': results}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reasoning/results/<reasoning_id>', methods=['GET'])
def get_reasoning_result(reasoning_id):
    """
    Get cached reasoning result by ID
    
    Returns: reasoning analysis object
    """
    try:
        result = reasoning_service.get_reasoning_by_id(reasoning_id)
        
        if not result:
            return jsonify({'error': 'Result not found'}), 404
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# APPLICATION TRACKER ENDPOINTS
# ============================================================================

@app.route('/api/applications', methods=['POST'])
def create_application():
    """Create new application tracking entry"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        application_data = {
            'opportunity_title': data.get('opportunity_title'),
            'opportunity_link': data.get('opportunity_link'),
            'deadline': data.get('deadline'),
            'status': 'saved',  # saved, applied, under_review, accepted, rejected
            'priority': data.get('priority', 'medium'),  # low, medium, high
            'notes': data.get('notes', ''),
            'eligibility_score': data.get('eligibility_score')
        }
        
        result = firebase_service.create_application(user_id, application_data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/applications/<user_id>', methods=['GET'])
def get_applications(user_id):
    """Get all applications for a user"""
    try:
        applications = firebase_service.get_user_applications(user_id)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/applications/<application_id>', methods=['PUT'])
def update_application(application_id):
    """Update application status"""
    try:
        data = request.json
        status = data.get('status')
        notes = data.get('notes')
        
        result = firebase_service.update_application_status(application_id, status, notes)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ELIGIBILITY SCORE ENDPOINTS
# ============================================================================

@app.route('/api/eligibility/calculate', methods=['POST'])
def calculate_eligibility():
    """Calculate eligibility score for opportunity"""
    try:
        data = request.json
        user_id = data.get('user_id')
        opportunity_data = data.get('opportunity')
        
        # Get user profile
        profile = firebase_service.get_profile(user_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Calculate score
        result = profile_service.calculate_eligibility_score(profile.get('profile', {}), opportunity_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# AI CHATBOT ENDPOINTS
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot messages"""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')
        context = data.get('context', {})  # Optional: current opportunity
        
        if not user_id or not message:
            return jsonify({'error': 'User ID and message required'}), 400
        
        # Auto-load user profile for personalized responses
        try:
            profile = firebase_service.get_user_profile(user_id)
            if profile:
                context['profile'] = profile
                print(f"✓ Loaded profile for chatbot: {profile.get('personal_info', {}).get('name', 'User')}")
        except Exception as profile_error:
            print(f"⚠️  Could not load profile for chatbot: {profile_error}")
        
        result = chatbot_service.chat(user_id, message, context)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/clear/<user_id>', methods=['POST'])
def clear_chat_history(user_id):
    """Clear chat history for user"""
    try:
        result = chatbot_service.clear_history(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# GAMIFICATION ENDPOINTS
# ============================================================================

@app.route('/api/gamification/<user_id>', methods=['GET'])
def get_gamification(user_id):
    """Get user's gamification profile"""
    try:
        result = gamification_service.get_user_gamification(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/gamification/action', methods=['POST'])
def award_points():
    """Award points for user action"""
    try:
        data = request.json
        user_id = data.get('user_id')
        action = data.get('action')
        metadata = data.get('metadata')
        
        if not user_id or not action:
            return jsonify({'error': 'user_id and action required'}), 400
        
        result = gamification_service.award_points(user_id, action, metadata)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/gamification/streak/<user_id>', methods=['POST'])
def update_streak(user_id):
    """Update daily login streak"""
    try:
        result = gamification_service.update_login_streak(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/gamification/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get global leaderboard with top 10 + current user"""
    try:
        user_id = request.args.get('user_id')  # Optional: to include current user
        top_limit = request.args.get('top', 10, type=int)  # Top N users
        
        result = gamification_service.get_leaderboard_with_user(top_limit, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.route('/api/analytics/<user_id>', methods=['GET'])
def get_analytics(user_id):
    """Get comprehensive analytics for user"""
    try:
        result = analytics_service.get_user_analytics(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({'error': 'No data found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/leaderboard/<user_id>', methods=['GET'])
def get_leaderboard_stats(user_id):
    """Get user's leaderboard position and surrounding users"""
    try:
        result = analytics_service.get_leaderboard_stats(user_id)
        if result:
            return jsonify(result), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/insights/<user_id>', methods=['GET'])
def get_insights(user_id):
    """Get personalized insights and recommendations"""
    try:
        result = analytics_service.get_insights(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Opportunity Intelligence API',
        'version': '1.0.0'
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """API information"""
    return jsonify({
        'name': 'AI-Powered Opportunity Intelligence System',
        'description': 'Never just say "Not Eligible" — Always explain why and guide how to improve',
        'endpoints': {
            'profiles': [
                'POST /api/profile/parse_resume',
                'POST /api/profile/create',
                'GET /api/profile/<id>'
            ],
            'opportunities': [
                'POST /api/opportunities/search',
                'GET /api/opportunities/cached',
                'GET /api/opportunities/<id>'
            ],
            'reasoning': [
                'POST /api/reasoning/analyze',
                'POST /api/reasoning/batch',
                'GET /api/reasoning/results/<id>'
            ]
        }
    }), 200


# ============================================================================
# SUCCESS STORIES & PEER INSIGHTS ENDPOINTS
# ============================================================================

@app.route('/api/success-stories', methods=['GET'])
def get_success_stories():
    """Get inspiring success stories from peers"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 5))
        
        stories = success_stories_service.get_success_stories(user_id, limit)
        
        return jsonify({
            'success': True,
            'stories': stories,
            'count': len(stories)
        }), 200
    
    except Exception as e:
        print(f"Error fetching success stories: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/peer-insights', methods=['GET'])
def get_peer_insights():
    """Get peer comparison and growth insights for healthy competition"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        insights = success_stories_service.get_peer_growth_insights(user_id)
        
        return jsonify({
            'success': True,
            'insights': insights
        }), 200
    
    except Exception as e:
        print(f"Error fetching peer insights: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  AI-Powered Opportunity Intelligence System                   ║
    ║  "Never just say 'Not Eligible' — Guide how to improve"      ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Server starting on http://localhost:{port}
    Environment: {'Development' if debug else 'Production'}
    """)
    
    # Disable auto-reload to prevent interruption during long-running requests (resume parsing)
    # Set use_reloader=False to avoid Flask restarting during file uploads
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
