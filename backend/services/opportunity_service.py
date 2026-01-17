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
        
        # Google Custom Search API credentials - Load all available keys
        self.search_api_keys = []
        for i in range(1, 10):  # Support up to 9 API keys
            key_name = 'GOOGLE_SEARCH_API_KEY' if i == 1 else f'GOOGLE_SEARCH_API_KEY_{i}'
            key_value = os.getenv(key_name)
            if key_value:
                self.search_api_keys.append(key_value)
        
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.current_key_index = 0  # Track which key we're using
        
        if not self.search_api_keys or not self.search_engine_id:
            print("⚠️  Warning: Google Search API credentials not configured")
        else:
            print(f"✓ Loaded {len(self.search_api_keys)} Google Search API key(s) for load balancing")
        
        self.search_url = "https://www.googleapis.com/customsearch/v1"
    
    def _get_next_api_key(self):
        """Get next API key in rotation"""
        if not self.search_api_keys:
            return None
        key = self.search_api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.search_api_keys)
        return key
    
    
    def generate_personalized_suggestions(self, profile_data):
        """
        Generate personalized search suggestions for ALL branches
        
        Args:
            profile_data: Student profile dictionary
        
        Returns:
            List of suggested search queries for all engineering/non-engineering students
        """
        suggestions = []
        
        # Extract key information
        skills = profile_data.get('skills', {})
        tech_skills = skills.get('technical', [])
        interests = profile_data.get('interests', [])
        education = profile_data.get('education', {})
        major = education.get('major', '').lower()
        degree = education.get('degree', '').lower()
        
        # Join all skills for easier matching
        all_skills = ' '.join(tech_skills).lower() if tech_skills else ''
        all_interests = ' '.join(interests).lower() if interests else ''
        combined_text = f"{major} {degree} {all_skills} {all_interests}"
        
        # === COMPUTER SCIENCE & IT ===
        cs_keywords = ['computer', 'software', 'it', 'information technology']
        if any(kw in combined_text for kw in cs_keywords):
            suggestions.append('Software development internship 2026')
            suggestions.append('Tech hackathon 2026')
        
        # === AI/ML/DATA SCIENCE ===
        ai_keywords = ['machine learning', 'ai', 'artificial intelligence', 'data science', 'deep learning']
        if any(kw in combined_text for kw in ai_keywords):
            suggestions.append('AI hackathon 2026')
            suggestions.append('Data Science competition 2026')
        
        # === MECHANICAL ENGINEERING ===
        mech_keywords = ['mechanical', 'automobile', 'automotive', 'manufacturing', 'cad', 'solidworks', 'catia']
        if any(kw in combined_text for kw in mech_keywords):
            suggestions.append('Mechanical engineering internship 2026')
            suggestions.append('Product design competition')
            suggestions.append('Automotive hackathon')
        
        # === ELECTRICAL/ELECTRONICS ===
        eee_keywords = ['electrical', 'electronics', 'ece', 'eee', 'circuit', 'vlsi', 'embedded', 'iot']
        if any(kw in combined_text for kw in eee_keywords):
            suggestions.append('Electronics project competition 2026')
            suggestions.append('IoT hackathon 2026')
            suggestions.append('Hardware engineering internship')
        
        # === CIVIL ENGINEERING ===
        civil_keywords = ['civil', 'construction', 'structural', 'architecture']
        if any(kw in combined_text for kw in civil_keywords):
            suggestions.append('Civil engineering internship 2026')
            suggestions.append('Infrastructure design competition')
            suggestions.append('Smart city hackathon')
        
        # === CHEMICAL/BIOTECHNOLOGY ===
        chem_keywords = ['chemical', 'biotech', 'biotechnology', 'pharmacy', 'pharmaceutical']
        if any(kw in combined_text for kw in chem_keywords):
            suggestions.append('Biotech innovation challenge 2026')
            suggestions.append('Chemical engineering internship')
            suggestions.append('Healthcare hackathon')
        
        # === BUSINESS/MANAGEMENT ===
        mgmt_keywords = ['management', 'mba', 'business', 'finance', 'marketing']
        if any(kw in combined_text for kw in mgmt_keywords):
            suggestions.append('Business case competition 2026')
            suggestions.append('Startup challenge')
            suggestions.append('Management internship 2026')
        
        # === DESIGN/CREATIVE ===
        design_keywords = ['design', 'ui', 'ux', 'graphic', 'creative']
        if any(kw in combined_text for kw in design_keywords):
            suggestions.append('Design competition 2026')
            suggestions.append('UI/UX hackathon')
        
        # === GENERAL FOR ALL STUDENTS ===
        # Always include general opportunities
        suggestions.extend([
            'Student hackathon 2026',
            'College internship program 2026',
            'Student fellowship 2026',
            'Innovation challenge',
            'Student startup competition'
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
    
    def _enhance_query(self, query, filters=None):
        """
        SIMPLIFIED query enhancement - less aggressive
        
        Args:
            query: Base query
            filters: Optional filters dictionary
        
        Returns:
            Enhanced query string
        """
        enhanced_parts = [query]
        
        # Add year filter if specified
        if filters and filters.get('deadline_year'):
            year = filters['deadline_year']
            enhanced_parts.append(f"{year}")
        
        # Simple domain targeting for common categories - OPTIONAL hints only
        # Don't force site: filter as it's too restrictive
        category_keywords = {
            'hackathon': 'competition coding challenge',
            'scholarship': 'scholarship funding grant',
            'internship': 'internship program training',
            'research': 'research fellowship program'
        }
        
        query_lower = query.lower()
        for category, keywords in category_keywords.items():
            if category in query_lower:
                enhanced_parts.append(keywords)
                break
        
        return ' '.join(enhanced_parts)
    
    
    def _perform_google_search(self, query, num_results=10):
        """
        Perform Google Custom Search API call with date filtering and pagination
        Fetches diverse results to avoid showing same opportunities
        Now includes India-specific filtering
        
        Args:
            query: Search query
            num_results: Number of results per page (max 10 per API call)
        
        Returns:
            Search results dictionary
        """
        if not self.search_api_keys or not self.search_engine_id:
            print("⚠️  Missing API credentials - using mock data")
            return self._get_mock_search_results(query)
        
        try:
            all_items = []
            
            # Fetch 2 pages for diverse results (2 pages = 20 results)
            # Reduced from 5 pages to save API quota
            for start_index in [1, 11]:
                # Get next API key in rotation
                api_key = self._get_next_api_key()
                
                params = {
                    'key': api_key,
                    'cx': self.search_engine_id,
                    'q': f"{query} India",  # Add India filter
                    'num': num_results,
                    'start': start_index,
                    'dateRestrict': 'm6',  # Last 6 months
                    'sort': 'date:d:s',
                    'gl': 'in',  # Geographic location: India
                    'cr': 'countryIN'  # Country restrict: India
                }
                
                print(f"🔍 Google Search (page {start_index}): {query} India")
                
                response = requests.get(self.search_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    items = result.get('items', [])
                    all_items.extend(items)
                    print(f"✅ Found {len(items)} results on page {start_index}")
                    
                    # Debug: Show API response if empty
                    if not items and start_index == 1:
                        print(f"⚠️  API Response: {result.get('searchInformation', {})}")
                        error = result.get('error', {})
                        if error:
                            print(f"❌ API Error: {error.get('message', 'Unknown error')}")
                            
                elif response.status_code == 429:
                    print(f"⚠️  Rate limit hit on API key #{self.current_key_index}")
                    print(f"   Used {len(all_items)} results so far from previous pages")
                    
                    # If we have other keys to try, continue with next key
                    if len(self.search_api_keys) > 1 and start_index == 1:
                        print(f"   Trying next API key in rotation...")
                        continue
                    else:
                        print(f"   All API keys exhausted or already have results, stopping search")
                        break
                else:
                    print(f"⚠️  API returned status {response.status_code} for page {start_index}")
                    try:
                        error_detail = response.json()
                        print(f"❌ Error details: {error_detail}")
                    except:
                        pass
                    # Continue to next page even if this one fails (unless it's the first page)
                    if start_index == 1:
                        print("❌ First page failed, stopping search")
                        break
                    else:
                        print("➡️  Continuing to next page...")
                        continue
            
            if not all_items:
                print("⚠️  No results from API - using mock data")
                return self._get_mock_search_results(query)
            
            print(f"✅ Total results fetched: {len(all_items)}")
            return {'items': all_items}
            
        except requests.RequestException as e:
            print(f"❌ Google Search API error: {e}")
            print("⚠️  Falling back to mock data")
            return self._get_mock_search_results(query)
    
    
    def _parse_search_results(self, search_results, opportunity_type=None):
        """
        Parse search results WITH relevance scoring and deadline filtering
        Removes expired opportunities based on deadline detection
        
        Args:
            search_results: Raw Google API response
            opportunity_type: Optional type filter
        
        Returns:
            List of structured opportunity dictionaries (only active/future events)
        """
        opportunities = []
        skipped_relevance = 0
        skipped_expired = 0
        
        items = search_results.get('items', [])
        print(f"📄 Parsing {len(items)} search results...")
        
        for idx, item in enumerate(items, 1):
            title = item.get('title', 'No title')
            link = item.get('link', '')
            snippet = item.get('snippet', 'No description')
            
            # Calculate relevance score (0-100)
            relevance_score = self._calculate_relevance_score(item)
            
            # More lenient filtering - accept if score > 15
            if relevance_score < 15:
                print(f"⏭️  Skipping #{idx}: Low relevance score {relevance_score} ({title[:50]}...)")
                skipped_relevance += 1
                continue
            
            # Check if opportunity has expired deadline
            if self._is_opportunity_expired(title, snippet):
                print(f"⏭️  Skipping #{idx}: Expired deadline ({title[:50]}...)")
                skipped_expired += 1
                continue
            
            # Infer type if not provided
            inferred_type = opportunity_type or self._infer_opportunity_type(title, snippet)
            
            # Extract opportunity details
            # Combine title and snippet for better deadline extraction
            combined_text = f"{title} {snippet}"
            deadline = self._extract_deadline(combined_text)
            
            opportunity = {
                'title': title,
                'link': link,
                'description': snippet,
                'snippet': snippet,
                'source': self._extract_domain(link),
                'relevance_score': relevance_score,
                'discovered_date': datetime.now().isoformat(),
                'type': inferred_type,
                'organizer': self._extract_organizer(title, snippet),
                'eligibility_text': self._extract_eligibility(snippet),
                'deadline': deadline or 'Not specified',
                'apply_by': deadline or 'Not specified',
                'opportunity_id': f"opp_{idx}",  # Use index for consistent IDs
                'url': link  # Add URL for ID generation
            }
            
            print(f"✅ Added #{idx}: {title[:50]}... (Score: {relevance_score})")
            opportunities.append(opportunity)
        
        # Sort by relevance score
        opportunities.sort(key=lambda x: x['relevance_score'], reverse=True)
        print(f"📊 Results: {len(opportunities)} kept, {skipped_relevance} low relevance, {skipped_expired} expired")
        
        # Save opportunities to database for eligibility checking
        try:
            import hashlib
            for opp in opportunities:
                # Use URL hash as ID for consistency and deduplication
                opp_id = hashlib.md5(opp['url'].encode()).hexdigest()[:12]
                opp['id'] = opp_id
                opp['opportunity_id'] = opp_id
                
                # Save to opportunities collection using firebase service
                self.firebase.db.collection('opportunities').document(opp_id).set({
                    'title': opp.get('title'),
                    'link': opp.get('link'),
                    'url': opp.get('url'),
                    'description': opp.get('description'),
                    'snippet': opp.get('snippet'),
                    'source': opp.get('source'),
                    'type': opp.get('type'),
                    'organizer': opp.get('organizer'),
                    'eligibility_text': opp.get('eligibility_text'),
                    'deadline': opp.get('deadline'),
                    'apply_by': opp.get('apply_by'),
                    'relevance_score': opp.get('relevance_score'),
                    'discovered_date': opp.get('discovered_date'),
                    'created_at': datetime.now().isoformat(),
                    'source_type': 'search',
                    'is_cached': True
                }, merge=True)
        except Exception as e:
            print(f"⚠️  Could not save opportunities to DB: {e}")
        
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
        Extract deadline date from snippet with extensive pattern matching
        Searches aggressively for any date mentions
        Returns formatted date string or None
        """
        from datetime import datetime
        import re
        
        # Look in both snippet (title + description are passed together)
        text = snippet
        
        # Extensive date patterns - catch everything possible
        date_patterns = [
            # With keywords
            (r'(?:deadline|apply by|last date|due date|register by|submit by|registration deadline|application deadline|closes on|close date|expiry|expires|ends on|till|before):?\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})', 'keyword_mdy'),
            (r'(?:deadline|apply by|last date|due date|register by|submit by|registration deadline|application deadline|closes on|close date|expiry|expires|ends on|till|before):?\s*(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})', 'keyword_dmy'),
            (r'(?:deadline|apply by|last date|due date|register by|submit by):?\s*(\d{1,2}\s+[A-Z][a-z]+\s+\'\d{2})', 'keyword_short_dmy'),
            (r'(?:deadline|apply by|last date|due date|register by|submit by):?\s*([A-Z][a-z]+\s+\d{1,2}\s+\'\d{2})', 'keyword_short_mdy'),
            
            # Standalone dates (more aggressive)
            (r'\b([A-Z][a-z]+\s+\d{1,2},?\s+20\d{2})\b', 'standalone_mdy'),
            (r'\b(\d{1,2}\s+[A-Z][a-z]+\s+20\d{2})\b', 'standalone_dmy'),
            (r'\b(\d{1,2}\s+[A-Z][a-z]+\s+\'\d{2})\b', 'standalone_short_dmy'),
            (r'\b([A-Z][a-z]+\s+\d{1,2}\s+\'\d{2})\b', 'standalone_short_mdy'),
            
            # Numeric formats
            (r'\b(\d{1,2}/\d{1,2}/20\d{2})\b', 'slash'),
            (r'\b(\d{1,2}-\d{1,2}-20\d{2})\b', 'dash'),
            (r'\b(20\d{2}-\d{1,2}-\d{1,2})\b', 'iso'),
        ]
        
        for pattern, date_type in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                
                # Convert short year to full year
                if "'" in date_str:
                    date_str = date_str.replace("'2", "202").replace("'1", "201")
                
                print(f"📅 Found deadline: {date_str}")
                return date_str
        
        print("⚠️  No deadline found in snippet")
        return None
    
    
    def _calculate_relevance_score(self, item):
        """
        Calculate relevance score (0-100) based on multiple factors
        
        Args:
            item: Search result item
        
        Returns:
            Relevance score (0-100)
        """
        score = 50  # Base score
        
        title = item.get('title', '').lower()
        snippet = item.get('snippet', '').lower()
        link = item.get('link', '').lower()
        
        # High-value keywords boost score
        high_value_keywords = ['apply', 'deadline', 'eligibility', 'register', 'prize', 'stipend', '2026']
        for keyword in high_value_keywords:
            if keyword in title:
                score += 5
            if keyword in snippet:
                score += 3
        
        # Trusted domains get boost
        trusted_domains = ['devpost.com', 'devfolio.co', 'unstop.com', 'internshala.com', 
                          'scholars4dev.com', 'opportunitydesk.org', 'linkedin.com']
        for domain in trusted_domains:
            if domain in link:
                score += 15
                break
        
        # Penalty for irrelevant indicators
        spam_indicators = ['login', 'signin', 'profile', 'settings', 'terms', 'privacy']
        for indicator in spam_indicators:
            if indicator in link:
                score -= 20
        
        return max(0, min(100, score))
    
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return 'Unknown'
    
    
    def _is_opportunity_expired(self, title, snippet):
        """
        Check if opportunity deadline has passed
        Dynamically calculates relative to today's date
        """
        from datetime import datetime, timedelta
        import re
        
        text = (title + ' ' + snippet).lower()
        current_date = datetime.now()
        
        # Look for "closed", "ended", "expired" keywords
        expired_keywords = ['closed', 'ended', 'expired', 'registration closed', 'applications closed']
        if any(keyword in text for keyword in expired_keywords):
            return True
        
        # Extract dates from text with multiple patterns
        date_patterns = [
            # Month Day, Year: Jan 15, 2026
            (r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* (\d{1,2}),? (\d{4})', 'mdy'),
            # Day-Month-Year: 15-01-2026 or 15/01/2026
            (r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})', 'dmy'),
            # Year-Month-Day: 2026-01-15
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', 'ymd'),
            # Deadline: 15 Jan 2026
            (r'deadline:?\s*(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(\d{4})', 'dmy_text'),
        ]
        
        month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                     'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
        
        for pattern, format_type in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    deadline = None
                    
                    if format_type == 'mdy':
                        # Month Day, Year
                        month = month_map.get(match[0][:3])
                        day = int(match[1])
                        year = int(match[2])
                        if month:
                            deadline = datetime(year, month, day)
                    
                    elif format_type == 'dmy':
                        # Day-Month-Year
                        day = int(match[0])
                        month = int(match[1])
                        year = int(match[2])
                        deadline = datetime(year, month, day)
                    
                    elif format_type == 'ymd':
                        # Year-Month-Day
                        year = int(match[0])
                        month = int(match[1])
                        day = int(match[2])
                        deadline = datetime(year, month, day)
                    
                    elif format_type == 'dmy_text':
                        # Day Month Year (text)
                        day = int(match[0])
                        month = month_map.get(match[1][:3])
                        year = int(match[2])
                        if month:
                            deadline = datetime(year, month, day)
                    
                    # Check if deadline is before yesterday
                    # Filter out anything with deadline on or before day before yesterday
                    yesterday = current_date - timedelta(days=1)
                    if deadline and deadline.date() < yesterday.date():
                        print(f"🚫 Expired: {deadline.date()} is before yesterday {yesterday.date()}")
                        return True
                        
                except Exception as e:
                    continue
        
        return False
    
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
        Updated with RECENT January 2026 active opportunities with future deadlines
        """
        return {
            'items': [
                {
                    'title': 'Google AI Hackathon 2026 - Build with Gemini | Unstop',
                    'link': 'https://unstop.com/hackathons/google-ai-hackathon-2026',
                    'snippet': 'Google AI Hackathon 2026 is now open! Build innovative AI solutions using Gemini API. Open to all students and developers. Eligibility: 18+ years, any background. Teams of 1-4 members. Prizes: ₹10 Lakhs + Google Cloud credits. Deadline: March 15, 2026. Apply now on Unstop!'
                },
                {
                    'title': 'Smart India Hackathon 2026 - Grand Finale | SIH',
                    'link': 'https://www.sih.gov.in/',
                    'snippet': 'Smart India Hackathon 2026 Grand Finale registrations open! Software and Hardware editions. Eligibility: Students enrolled in recognized institutions, teams of 6. Problem statements released January 2026. Internal hackathons: Feb-March 2026. Grand Finale: April 2026. Registration deadline: February 20, 2026.'
                },
                {
                    'title': 'Microsoft Imagine Cup 2026 India Finals | Microsoft',
                    'link': 'https://imaginecup.microsoft.com/india',
                    'snippet': 'Microsoft Imagine Cup 2026 India Round is accepting submissions! Categories: AI for Good, Gaming, Mixed Reality. Eligibility: Students 16+, teams up to 4. Build solutions addressing UN SDGs. India regional deadline: March 31, 2026. Winners advance to World Finals with $100K prize. Start building today!'
                },
                {
                    'title': 'ETHIndia 2026 - Devfolio | Ethereum Foundation',
                    'link': 'https://devfolio.co/ethindia2026',
                    'snippet': 'ETHIndia 2026 applications are open! India\'s largest Ethereum hackathon. 36-hour in-person event in Bangalore. Eligibility: Developers, designers, blockchain enthusiasts 18+. No prior blockchain experience needed. Mentorship from Ethereum Foundation. Event dates: March 14-16, 2026. Apply by: February 25, 2026.'
                },
                {
                    'title': 'MLH Season 2026 India Region - Major League Hacking',
                    'link': 'https://mlh.io/seasons/2026/events',
                    'snippet': 'Major League Hacking Season 2026 India events! HackNITR (Feb 24-26), VITHack (Mar 7-9), HackOdisha (Mar 21-23), PesHack (Apr 7-9). Open to all students. Free participation, travel reimbursements available. Build projects in 24-36 hours. MLH swag, prizes, and networking. Register now!'
                },
                {
                    'title': 'Amazon ML Challenge 2026 | Amazon India Careers',
                    'link': 'https://amazonmlchallenge.com/',
                    'snippet': 'Amazon ML Challenge 2026 is live! Solve real-world machine learning problems. Eligibility: Engineering/MCA students, 2025-2027 graduates. Individual participation. Prizes: ₹1 Lakh + interview opportunity. Phase 1: February 1-28, 2026. Phase 2: March 2026. Winners announced April 2026. Apply now!'
                },
                {
                    'title': 'Tata Innoverse 2026 - Innovation Challenge | Tata Group',
                    'link': 'https://innoverse.tata.com/',
                    'snippet': 'Tata Innoverse 2026 accepting entries! Pan-India innovation challenge for students and startups. Categories: Healthcare, Education, Sustainability, Smart Cities. Eligibility: Students 18+, startups < 3 years. Teams of 2-5. Prizes: ₹15 Lakhs + mentorship. Submission deadline: March 10, 2026. Submit your innovation!'
                },
                {
                    'title': 'KIIT Hackathon 2026 - KiiT University | Unstop',
                    'link': 'https://unstop.com/hackathons/kiit-hackathon-2026',
                    'snippet': 'KIIT Hackathon 2026 registrations open! 48-hour mega hackathon at KIIT University, Bhubaneswar. Tracks: AI/ML, Blockchain, IoT, Web3. Eligibility: All college students across India. Teams of 3-4. Accommodation provided. Prizes worth ₹5 Lakhs. Event: February 28 - March 2, 2026. Register by: February 15, 2026.'
                },
                {
                    'title': 'Code For Good 2026 - JP Morgan Chase | JPMC Careers',
                    'link': 'https://careers.jpmorgan.com/codeforgood',
                    'snippet': 'JP Morgan Code For Good 2026 applications open! 24-hour hackathon building tech solutions for non-profits. Eligibility: Engineering students graduating 2026/2027, all branches. Team formation at event. Cities: Mumbai, Bangalore, Hyderabad. Event dates: March 15-16, 2026. Apply by: February 20, 2026. Travel covered!'
                },
                {
                    'title': 'IEEE Student Congress 2026 - International Conference',
                    'link': 'https://ieee-student-congress.org/',
                    'snippet': 'IEEE Student Congress 2026 call for papers! Submit research in Electronics, Computer Science, AI, IoT, Robotics. Eligibility: UG/PG students, IEEE members preferred. Paper submission: January 20 - March 1, 2026. Conference: April 12-14, 2026, IIT Delhi. Publish in IEEE Xplore. Early bird: February 15.'
                }
            ]
        }
