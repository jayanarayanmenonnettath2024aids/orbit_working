"""
Reasoning Service - Core AI intelligence using Gemini API
Analyzes student eligibility and generates guidance
"""

import os
import google.generativeai as genai
import json
import re
from typing import Dict, List


class ReasoningService:
    def __init__(self, firebase_service):
        """
        Initialize Reasoning Service with Gemini AI
        
        Args:
            firebase_service: FirebaseService instance
        """
        self.firebase = firebase_service
        
        # Configure Gemini API with load balancing
        gemini_key = os.getenv('GEMINI_API_KEY')
        gemini_key_2 = os.getenv('GEMINI_API_KEY_2')
        
        # Setup key rotation for load balancing
        self.api_keys = [k for k in [gemini_key, gemini_key_2] if k]
        if not self.api_keys:
            print("⚠️  Warning: No GEMINI_API_KEY configured")
        elif len(self.api_keys) == 2:
            print(f"✓ Load balancing enabled with {len(self.api_keys)} Gemini API keys")
        
        self.current_key_index = 0
        self._configure_current_key()
    
    def _configure_current_key(self):
        """Configure Gemini with current API key"""
        if self.api_keys:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def _rotate_key(self):
        """Rotate to next API key for load balancing"""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            self._configure_current_key()
    
    
    def analyze_eligibility(self, profile_id: str, opportunity_id: str) -> Dict:
        """
        Analyze student eligibility for an opportunity using Gemini AI
        
        Args:
            profile_id: Student profile ID
            opportunity_id: Opportunity ID
        
        Returns:
            Dictionary with structured eligibility analysis
        """
        try:
            # Fetch profile and opportunity
            profile = self.firebase.get_student_profile(profile_id)
            opportunity = self.firebase.get_opportunity(opportunity_id)
            
            if not profile:
                raise Exception(f"Profile {profile_id} not found")
            
            if not opportunity:
                raise Exception(f"Opportunity {opportunity_id} not found")
            
            print(f"Analyzing eligibility for profile {profile_id} and opportunity {opportunity_id}")
            
            # Perform AI reasoning
            analysis = self._perform_gemini_reasoning(
                profile['profile'],
                opportunity
            )
            
            if not analysis:
                print("Warning: Gemini returned empty analysis, using fallback")
                analysis = self._create_fallback_analysis()
            
            # Store result in Firebase
            result = self.firebase.create_reasoning_result(
                profile_id,
                opportunity_id,
                analysis
            )
            
            return result
            
        except Exception as e:
            print(f"Error in analyze_eligibility: {str(e)}")
            # Return fallback analysis instead of crashing
            fallback = self._create_fallback_analysis()
            try:
                result = self.firebase.create_reasoning_result(
                    profile_id,
                    opportunity_id,
                    fallback
                )
                return result
            except:
                # If Firebase also fails, return the fallback directly
                return {
                    'reasoning_id': 'fallback',
                    'analysis': fallback,
                    'analyzed_at': None
                }
    
    
    def analyze_batch(self, profile_id: str, opportunity_ids: List[str]) -> List[Dict]:
        """
        Analyze eligibility for multiple opportunities at once
        
        Args:
            profile_id: Student profile ID
            opportunity_ids: List of opportunity IDs
        
        Returns:
            List of analysis results
        """
        results = []
        
        for opp_id in opportunity_ids:
            try:
                # Check cache first
                cached = self.get_cached_reasoning(profile_id, opp_id)
                if cached:
                    results.append({
                        'opportunity_id': opp_id,
                        'analysis': cached['analysis'],
                        'cached': True
                    })
                else:
                    # Perform new analysis
                    analysis = self.analyze_eligibility(profile_id, opp_id)
                    results.append({
                        'opportunity_id': opp_id,
                        'analysis': analysis,
                        'cached': False
                    })
            except Exception as e:
                results.append({
                    'opportunity_id': opp_id,
                    'error': str(e)
                })
        
        return results
    
    
    def get_cached_reasoning(self, profile_id: str, opportunity_id: str):
        """
        Check if reasoning already exists (cached)
        """
        return self.firebase.get_cached_reasoning(profile_id, opportunity_id)
    
    
    def get_reasoning_by_id(self, reasoning_id: str):
        """
        Get reasoning result by ID
        """
        return self.firebase.get_reasoning_result(reasoning_id)
    
    
    # ========================================================================
    # CORE AI REASONING WITH GEMINI
    # ========================================================================
    
    def _perform_gemini_reasoning(self, profile_data: Dict, opportunity: Dict) -> Dict:
        """
        Use Gemini API to perform eligibility reasoning
        
        Args:
            profile_data: Structured student profile
            opportunity: Opportunity details
        
        Returns:
            Structured analysis dictionary
        """
        # Build prompt using template
        prompt = self._build_reasoning_prompt(profile_data, opportunity)
        
        try:
            print(f"Calling Gemini API for reasoning...")
            
            # Call Gemini API
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 2048,
                }
            )
            
            # Rotate API key for load balancing
            self._rotate_key()
            
            print(f"Gemini API responded successfully")
            
            # Parse JSON response
            response_text = response.text.strip()
            
            if not response_text:
                print("Warning: Empty response from Gemini")
                return self._create_fallback_analysis()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = re.sub(r'^```(?:json)?\n', '', response_text)
                response_text = re.sub(r'\n```$', '', response_text)
            
            # Remove any trailing commas before closing braces/brackets
            response_text = re.sub(r',\s*}', '}', response_text)
            response_text = re.sub(r',\s*]', ']', response_text)
            
            # Fix common JSON issues
            response_text = response_text.replace('\n', ' ')
            
            print(f"Parsing JSON response (length: {len(response_text)})")
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            # Validate structure
            self._validate_analysis_structure(analysis)
            
            print(f"Successfully parsed and validated analysis")
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print(f"Response was: {response_text[:500] if 'response_text' in locals() else 'No response'}")
            # Return fallback response
            return self._create_fallback_analysis()
        
        except Exception as e:
            print(f"Gemini reasoning failed: {e}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_analysis()
    
    
    def _build_reasoning_prompt(self, profile_data: Dict, opportunity: Dict) -> str:
        """
        Build detailed prompt for Gemini eligibility reasoning
        
        Uses the prompt template from GEMINI_PROMPTS.md
        """
        # Convert profile to JSON string
        profile_json = json.dumps(profile_data, indent=2)
        
        # Extract opportunity details
        title = opportunity.get('title', 'Unknown Opportunity')
        organizer = opportunity.get('organizer', 'Unknown Organizer')
        eligibility_text = opportunity.get('eligibility_text', opportunity.get('snippet', ''))
        
        prompt = f"""
You are an expert career advisor and opportunity analyst specializing in helping students in Tier-2 and Tier-3 colleges in India understand their eligibility for opportunities.

Your role is NOT to gatekeep, but to:
- Explain eligibility transparently
- Identify gaps constructively
- Provide actionable guidance
- Encourage growth mindset

---

STUDENT PROFILE:
```json
{profile_json}
```

OPPORTUNITY DETAILS:
Title: {title}
Organizer: {organizer}
Eligibility Criteria (Raw Text):
```
{eligibility_text}
```

---

TASK:
Analyze whether this student meets the eligibility criteria.

OUTPUT REQUIREMENTS:
Return ONLY valid JSON in this exact structure:

{{
  "eligibility_status": "<one of: Eligible | Partially Eligible | Not Yet Eligible>",
  "reasons_met": [
    "List each criterion the student MEETS with specific evidence from their profile"
  ],
  "reasons_not_met": [
    "List each criterion the student DOES NOT MEET with clear explanation"
  ],
  "missing_skills": [
    "Specific technical or soft skills the student needs to acquire"
  ],
  "missing_experience": [
    "Types of experience the student lacks (projects, internships, leadership, etc.)"
  ],
  "confidence_score": <integer 0-100>,
  "explanation_simple": "<2-3 sentence plain English explanation a student would understand>",
  "next_steps": [
    {{
      "action": "<Specific, actionable step>",
      "reason": "<Why this matters for this opportunity>",
      "time_estimate": "<Realistic timeframe: e.g., '2-3 weeks', '1 month', '3-6 months'>"
    }}
  ]
}}

---

CRITICAL RULES:
1. NEVER say just "not eligible" without explanation
2. Be encouraging, not discouraging—frame gaps as development opportunities
3. Use simple, mentor-like language (avoid academic jargon)
4. Be specific about what's missing (not vague like "improve skills")
5. If criteria are ambiguous, interpret generously in favor of the student
6. If confidence is low (<60), acknowledge uncertainty in explanation
7. Focus next_steps on skill-building, project ideas, or community engagement
8. Keep explanation_simple under 100 words
9. Limit next_steps to 3-5 most impactful actions
10. Always output valid, parseable JSON

---

NOW ANALYZE THE STUDENT PROFILE AND OPPORTUNITY PROVIDED ABOVE.
OUTPUT ONLY THE JSON. DO NOT ADD ANY EXTRA TEXT BEFORE OR AFTER THE JSON.
"""
        
        return prompt
    
    
    def _validate_analysis_structure(self, analysis: Dict):
        """
        Validate that Gemini response has correct structure
        
        Raises:
            Exception if structure is invalid
        """
        required_fields = [
            'eligibility_status',
            'reasons_met',
            'reasons_not_met',
            'missing_skills',
            'missing_experience',
            'confidence_score',
            'explanation_simple',
            'next_steps'
        ]
        
        for field in required_fields:
            if field not in analysis:
                raise Exception(f"Analysis missing required field: {field}")
        
        # Validate types
        if not isinstance(analysis['reasons_met'], list):
            raise Exception("reasons_met must be an array")
        
        if not isinstance(analysis['next_steps'], list):
            raise Exception("next_steps must be an array")
        
        if not isinstance(analysis['confidence_score'], (int, float)):
            raise Exception("confidence_score must be a number")
        
        return True
    
    
    def _create_fallback_analysis(self) -> Dict:
        """
        Create fallback analysis when Gemini fails
        """
        return {
            "eligibility_status": "Partially Eligible",
            "reasons_met": [
                "Your profile shows potential and enthusiasm"
            ],
            "reasons_not_met": [
                "Unable to fully analyze eligibility criteria at this time"
            ],
            "missing_skills": [],
            "missing_experience": [],
            "confidence_score": 50,
            "explanation_simple": "We're having trouble analyzing your full eligibility right now, but your profile shows promise. We recommend reviewing the opportunity details directly and reaching out to the organizers with questions.",
            "next_steps": [
                {
                    "action": "Review the opportunity details on their official website",
                    "reason": "Get complete information about requirements and how to apply",
                    "time_estimate": "30 minutes"
                },
                {
                    "action": "Contact the organizers directly with your questions",
                    "reason": "They can provide personalized guidance on your eligibility",
                    "time_estimate": "1 day"
                }
            ]
        }
    
    
    # ========================================================================
    # ADDITIONAL REASONING UTILITIES
    # ========================================================================
    
    def generate_personalized_guidance(self, profile_id: str, gap_analysis: Dict) -> Dict:
        """
        Generate more detailed, personalized guidance based on gaps
        
        This is an optional enhancement for more tailored advice
        """
        profile = self.firebase.get_student_profile(profile_id)
        
        if not profile:
            return {"error": "Profile not found"}
        
        # Build guidance prompt
        prompt = f"""
You are a mentor helping a student in India prepare for opportunities.

STUDENT SITUATION:
- Skills they're missing: {', '.join(gap_analysis.get('missing_skills', []))}
- Experience gaps: {', '.join(gap_analysis.get('missing_experience', []))}

Generate 3-5 specific, practical steps this student can take.

REQUIREMENTS:
- Actionable (not vague)
- Doable with limited resources
- Time-bound
- Encouraging

OUTPUT (JSON):
{{
  "personalized_steps": [
    {{
      "action": "...",
      "why": "...",
      "time": "...",
      "resources": ["Free resource 1", "Free resource 2"]
    }}
  ]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            return {"error": str(e)}
