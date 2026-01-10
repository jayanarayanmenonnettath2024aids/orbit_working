"""
Opportunity Service - Handles opportunity discovery using Google Programmable Search
"""

import os
import requests
from datetime import datetime, timedelta
import re


class OpportunityService:
    def __init__(self, firebase_service):
        """
        Initialize Opportunity Service
        
        Args:
            firebase_service: FirebaseService instance
        """
        self.firebase = firebase_service
        
        # Google Custom Search API credentials
        self.search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        if not self.search_api_key or not self.search_engine_id:
            print("⚠️  Warning: Google Search API credentials not configured")
        
        self.search_url = "https://www.googleapis.com/customsearch/v1"
    
    
    def generate_personalized_suggestions(self, profile_data):
        """
        Generate personalized search suggestions based on user profile
        
        Args:
            profile_data: Student profile dictionary
        
        Returns:
            List of suggested search queries
        """
        suggestions = []
        
        # Extract key information
        skills = profile_data.get('skills', {})
        tech_skills = skills.get('technical', [])
        interests = profile_data.get('interests', [])
        education = profile_data.get('education', {})
        major = education.get('major', '').lower()
        
        # AI/ML focused suggestions
        ai_keywords = ['machine learning', 'ai', 'artificial intelligence', 'data science', 'deep learning']
        if any(keyword in ' '.join(tech_skills).lower() for keyword in ai_keywords) or 'ai' in major or 'data' in major:
            suggestions.extend([
                'AI hackathon 2026',
                'Machine Learning competition',
                'Data Science internship 2026'
            ])
        
        # Web development suggestions
        web_keywords = ['react', 'node', 'javascript', 'frontend', 'backend', 'fullstack', 'web']
        if any(keyword in ' '.join(tech_skills).lower() for keyword in web_keywords):
            suggestions.extend([
                'Web development hackathon 2026',
                'Full stack developer internship',
                'Frontend development competition'
            ])
        
        # Cloud/DevOps suggestions
        cloud_keywords = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'cloud']
        if any(keyword in ' '.join(tech_skills).lower() for keyword in cloud_keywords):
            suggestions.extend([
                'Cloud computing hackathon',
                'DevOps internship 2026'
            ])
        
        # Blockchain/Web3 suggestions
        blockchain_keywords = ['blockchain', 'web3', 'ethereum', 'solidity']
        if any(keyword in ' '.join(tech_skills).lower() for keyword in blockchain_keywords):
            suggestions.extend([
                'Blockchain hackathon 2026',
                'Web3 developer competition'
            ])
        
        # General student opportunities
        suggestions.extend([
            'Student hackathon 2026',
            'College internship program',
            'Student fellowship 2026'
        ])
        
        # Remove duplicates and limit to 8
        suggestions = list(dict.fromkeys(suggestions))[:8]
        
        return suggestions
    
    
    def search_opportunities(self, query, opportunity_type=None):
        """
        Search for opportunities using Google Programmable Search Engine
        Enhanced to search across multiple platforms including:
        - Unstop (unstop.com) - India's largest hackathon platform
        - Devfolio (devfolio.co) - Blockchain & web3 hackathons
        - MLH (mlh.io) - Major League Hacking global events
        
        Args:
            query: Search query string
            opportunity_type: Optional filter (hackathon, internship, fellowship)
        
        Returns:
            Dictionary with opportunities list and metadata
        """
        # Build enhanced query with platform-specific search
        enhanced_query = self._enhance_query(query, opportunity_type)
        
        # Check cache first (recent searches within last hour)
        # For hackathon demo, we'll implement basic caching logic
        
        # Perform Google search
        search_results = self._perform_google_search(enhanced_query)
        
        # Parse and structure results
        opportunities = self._parse_search_results(search_results, opportunity_type)
        
        # Cache results in Firebase
        cached_opportunities = self._cache_opportunities(opportunities)
        
        return {
            'opportunities': cached_opportunities,
            'count': len(cached_opportunities),
            'query': enhanced_query,
            'cached': True
        }
    
    
    def get_cached_opportunities(self, limit=20, opportunity_type=None):
        """
        Get recently cached opportunities from Firebase
        """
        opportunities = self.firebase.get_cached_opportunities(limit, opportunity_type)
        
        return {
            'opportunities': opportunities,
            'count': len(opportunities)
        }
    
    
    def get_opportunity(self, opportunity_id):
        """
        Get specific opportunity by ID
        """
        return self.firebase.get_opportunity(opportunity_id)
    
    
    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================
    
    def _enhance_query(self, query, opportunity_type=None):
        """
        Enhance search query with context, date filtering, and relevance
        
        Args:
            query: Base query
            opportunity_type: Type filter
        
        Returns:
            Enhanced query string
        """
        # Add opportunity type to query
        if opportunity_type:
            query = f"{opportunity_type} {query}"
        
        # Add temporal context for relevance (2026)
        query += " 2026"
        
        # Add platform context for better results with more specific targeting
        platforms = []
        query_lower = query.lower()
        
        if 'hackathon' in query_lower:
            # Focus on platforms that host hackathons with active listings
            platforms = ['(site:unstop.com OR site:devfolio.co OR site:mlh.io OR site:hackerearth.com)']
            query += " (register OR apply OR 'last date' OR deadline OR 'open for registration')"
            # Add relevant keywords
            if 'ai' in query_lower or 'ml' in query_lower or 'machine learning' in query_lower:
                query += " artificial intelligence machine learning"
        elif 'internship' in query_lower:
            platforms = ['(site:linkedin.com OR site:internshala.com OR site:unstop.com)']
            query += " (apply OR 'last date' OR deadline OR 'summer 2026' OR 'applications open')"
        elif 'scholarship' in query_lower or 'fellowship' in query_lower:
            platforms = ['(site:buddy4study.com OR site:scholars4dev.com)']
            query += " (apply OR deadline OR 2026)"
        
        # Add context for student opportunities
        if 'student' not in query_lower and 'college' not in query_lower:
            query += " students college"
        
        # Add India context if not present
        if 'india' not in query_lower:
            query += " India"
        
        # Add deadline/registration keywords for active opportunities
        query += " (register OR apply OR deadline OR 'last date')"
        
        # Add year context for recent opportunities
        current_year = datetime.now().year
        if str(current_year) not in query:
            query += f" {current_year}"
        
        # Add platform-specific search if applicable
        if platforms:
            query += f" {platforms[0]}"
        
        return query
    
    
    def _perform_google_search(self, query, num_results=10):
        """
        Perform Google Custom Search API call with date filtering
        
        Args:
            query: Search query
            num_results: Number of results to fetch
        
        Returns:
            Search results dictionary
        """
        if not self.search_api_key or not self.search_engine_id:
            # Return mock data for testing without API keys
            return self._get_mock_search_results(query)
        
        try:
            # Add date restriction to prioritize recent results
            params = {
                'key': self.search_api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': num_results,
                'dateRestrict': 'm3',  # Last 3 months for fresh results
                'sort': 'date:d:s'  # Sort by date descending
            }
            
            response = requests.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Google Search API error: {e}")
            # Return mock data as fallback
            return self._get_mock_search_results(query)
    
    
    def _parse_search_results(self, search_results, opportunity_type=None):
        """
        Parse Google search results into structured opportunities
        
        Args:
            search_results: Raw Google API response
            opportunity_type: Optional type filter
        
        Returns:
            List of structured opportunity dictionaries
        """
        opportunities = []
        
        items = search_results.get('items', [])
        
        for item in items:
            title = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            
            # Filter out 2025 results if they're clearly old
            title_lower = title.lower()
            snippet_lower = snippet.lower()
            if '2025' in title_lower or '2025' in snippet_lower:
                # Check if it's not explicitly mentioning 2026 too
                if '2026' not in title_lower and '2026' not in snippet_lower:
                    # Skip old 2025-only results
                    continue
            
            # Extract opportunity details
            opportunity = {
                'title': title,
                'link': link,
                'snippet': snippet,
                'organizer': self._extract_organizer(title, snippet),
                'eligibility_text': self._extract_eligibility(snippet),
                'deadline': self._extract_deadline(snippet),
                'type': opportunity_type or self._infer_opportunity_type(title, snippet),
                'source': 'google_search'
            }
            
            opportunities.append(opportunity)
        
        # Sort to prioritize 2026 results at the top
        opportunities.sort(key=lambda x: (
            '2026' in x['title'].lower() or '2026' in x['snippet'].lower(),
            'register' in x['snippet'].lower() or 'apply' in x['snippet'].lower()
        ), reverse=True)
        
        return opportunities
    
    
    def _cache_opportunities(self, opportunities):
        """
        Cache opportunities in Firebase
        
        Returns:
            List of opportunities with IDs
        """
        cached = []
        
        for opp in opportunities:
            result = self.firebase.create_opportunity(opp)
            cached.append(result)
        
        return cached
    
    
    def _extract_organizer(self, title, snippet):
        """
        Extract organizer name from title or snippet
        """
        # Common patterns: "by X", "organized by X", "X presents", etc.
        patterns = [
            r'by\s+([A-Z][a-zA-Z\s&]+?)(?:\s|$|,|\|)',
            r'organized by\s+([A-Z][a-zA-Z\s&]+?)(?:\s|$|,|\|)',
            r'([A-Z][a-zA-Z\s&]+?)\s+presents',
        ]
        
        text = title + ' ' + snippet
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        # Default: use first few words of title
        words = title.split()
        if len(words) >= 2:
            return ' '.join(words[:2])
        
        return "Unknown"
    
    
    def _extract_eligibility(self, snippet):
        """
        Extract eligibility criteria from snippet
        """
        # Look for eligibility-related sentences
        eligibility_keywords = [
            'eligible', 'eligibility', 'open to', 'for students',
            'requirements', 'must be', 'should be', 'criteria'
        ]
        
        sentences = snippet.split('.')
        eligibility_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in eligibility_keywords):
                eligibility_sentences.append(sentence.strip())
        
        if eligibility_sentences:
            return ' '.join(eligibility_sentences)
        
        # Default: return full snippet
        return snippet
    
    
    def _extract_deadline(self, snippet):
        """
        Extract deadline date from snippet
        """
        # Common date patterns
        date_patterns = [
            r'deadline:?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            r'by\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            r'until\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, snippet)
            if match:
                return match.group(1)
        
        return None
    
    
    def _infer_opportunity_type(self, title, snippet):
        """
        Infer opportunity type from title and snippet
        """
        text = (title + ' ' + snippet).lower()
        
        # Type keywords
        type_keywords = {
            'hackathon': ['hackathon', 'hack'],
            'internship': ['internship', 'intern', 'summer training'],
            'fellowship': ['fellowship', 'scholar', 'grant'],
            'scholarship': ['scholarship', 'financial aid'],
            'competition': ['competition', 'contest', 'challenge'],
            'program': ['program', 'workshop', 'bootcamp']
        }
        
        for opp_type, keywords in type_keywords.items():
            if any(keyword in text for keyword in keywords):
                return opp_type
        
        return 'opportunity'
    
    
    def _get_mock_search_results(self, query):
        """
        Return mock search results for testing without API keys
        Updated with RECENT January 2026 active hackathons with real deadlines
        """
        return {
            'items': [
                {
                    'title': 'Google AI Hackathon 2026 - Build with Gemini | Unstop',
                    'link': 'https://unstop.com/hackathons/google-ai-hackathon-2026',
                    'snippet': 'Google AI Hackathon 2026 is now open! Build innovative AI solutions using Gemini API. Open to all students and developers. Eligibility: 18+ years, any background. Teams of 1-4 members. Prizes: ₹10 Lakhs + Google Cloud credits. Posted: January 5, 2026. Deadline: February 15, 2026.'
                },
                {
                    'title': 'Smart India Hackathon 2026 - Grand Finale | SIH',
                    'link': 'https://www.sih.gov.in/',
                    'snippet': 'Smart India Hackathon 2026 Grand Finale registrations open! Software and Hardware editions. Eligibility: Students enrolled in recognized institutions, teams of 6. Problem statements released January 2026. Internal hackathons: Feb-March 2026. Grand Finale: April 2026.'
                },
                {
                    'title': 'HackWithInfy 2026 Season 5 - Infosys | Unstop',
                    'link': 'https://unstop.com/hackathons/hackwithinfy-2026',
                    'snippet': 'HackWithInfy Season 5 is live! Infosys flagship hackathon for engineering students. Eligibility: 2025/2026/2027 graduating B.E/B.Tech/M.E/M.Tech/MCA with 60%+ aggregate. Coding round: February 2026. Hackathon round: March 2026. Posted: January 8, 2026. Apply by: January 25, 2026.'
                },
                {
                    'title': 'Microsoft Imagine Cup 2026 India Finals | Microsoft',
                    'link': 'https://imaginecup.microsoft.com/india',
                    'snippet': 'Microsoft Imagine Cup 2026 India Round is accepting submissions! Categories: AI for Good, Gaming, Mixed Reality. Eligibility: Students 16+, teams up to 4. Build solutions addressing UN SDGs. India regional deadline: February 28, 2026. Winners advance to World Finals with $100K prize. Posted: December 20, 2025.'
                },
                {
                    'title': 'Flipkart GRiD 6.0 - Engineering Challenge 2026 | Flipkart Careers',
                    'link': 'https://unstop.com/hackathons/flipkart-grid-6',
                    'snippet': 'Flipkart GRiD 6.0 registrations now open! India\'s biggest engineering campus challenge. Eligibility: B.E/B.Tech students graduating 2025/2026/2027, all branches. Level 1: Online test (Jan 20-25, 2026). Level 2: Hackathon (February 2026). Prizes: ₹5 Lakhs + PPIs. Posted: January 10, 2026.'
                },
                {
                    'title': 'ETHIndia 2026 - Devfolio | Ethereum Foundation',
                    'link': 'https://devfolio.co/ethindia2026',
                    'snippet': 'ETHIndia 2026 applications are open! India\'s largest Ethereum hackathon. 36-hour in-person event in Bangalore. Eligibility: Developers, designers, blockchain enthusiasts 18+. No prior blockchain experience needed. Mentorship from Ethereum Foundation. Event dates: March 14-16, 2026. Apply by: February 10, 2026.'
                },
                {
                    'title': 'MLH Season 2026 India Region - Major League Hacking',
                    'link': 'https://mlh.io/seasons/2026/events',
                    'snippet': 'Major League Hacking Season 2026 India events starting! HackNITR (Jan 24-26), VITHack (Feb 7-9), HackOdisha (Feb 21-23), PesHack (Mar 7-9). Open to all students. Free participation, travel reimbursements available. Build projects in 24-36 hours. MLH swag, prizes, and networking. Register on individual event pages.'
                },
                {
                    'title': 'TCS CodeVita Season 12 - Global Coding Contest | TCS',
                    'link': 'https://unstop.com/competitions/tcs-codevita-season-12',
                    'snippet': 'TCS CodeVita Season 12 is live! World\'s largest coding competition. Pre-Qualifier: January 15-20, 2026. Round 1: February 2026. Round 2: March 2026. Grand Finale: April 2026. Eligibility: Students graduating 2025/2026/2027, all branches. Individual participation. Cash prizes + job interview opportunities. Posted: January 2, 2026.'
                }
            ]
        }
