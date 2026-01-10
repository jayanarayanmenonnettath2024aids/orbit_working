"""
Main Flask application for AI-Powered Opportunity Intelligence System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import services
from services.profile_service import ProfileService
from services.opportunity_service import OpportunityService
from services.reasoning_service import ReasoningService
from services.firebase_service import FirebaseService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
firebase_service = FirebaseService()
profile_service = ProfileService(firebase_service)
opportunity_service = OpportunityService(firebase_service)
reasoning_service = ReasoningService(firebase_service)

# ============================================================================
# PROFILE ENDPOINTS
# ============================================================================

@app.route('/api/profile/parse_resume', methods=['POST'])
def parse_resume():
    """
    Parse resume PDF and create structured profile
    
    Expected: multipart/form-data with 'resume' file
    Returns: { profile_id, profile_data }
    """
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Parse and create profile
        result = profile_service.parse_and_create_profile(resume_file)
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    Search for opportunities using Google Programmable Search
    
    Expected JSON:
    {
        "query": "AI hackathon India",
        "opportunity_type": "hackathon"  // optional
    }
    
    Returns: { opportunities: [...], count, cached }
    """
    try:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query required'}), 400
        
        query = data['query']
        opportunity_type = data.get('opportunity_type', None)
        
        # Search opportunities
        result = opportunity_service.search_opportunities(query, opportunity_type)
        
        return jsonify(result), 200
        
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
    
    app.run(host='0.0.0.0', port=port, debug=debug)
