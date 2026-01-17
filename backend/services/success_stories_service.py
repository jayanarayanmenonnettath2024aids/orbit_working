"""Success Stories Service - Inspire users with peer achievements"""
from datetime import datetime, timedelta
import random


class SuccessStoriesService:
    def __init__(self, firebase):
        self.firebase = firebase
        
    def get_success_stories(self, user_id, limit=5):
        """Get inspiring success stories from peers who achieved real results"""
        try:
            db = self.firebase.db
            
            # First, try to find real success stories from actual users
            real_stories = self._find_real_success_stories(db, user_id, limit)
            
            # If not enough real stories, supplement with synthetic ones
            if len(real_stories) < limit:
                synthetic_needed = limit - len(real_stories)
                synthetic_stories = self._get_synthetic_success_stories(synthetic_needed)
                return real_stories + synthetic_stories
            
            return real_stories[:limit]
        
        except Exception as e:
            print(f"Error fetching success stories: {str(e)}")
            # Fallback to synthetic stories
            return self._get_synthetic_success_stories(limit)
    
    def _find_real_success_stories(self, db, user_id, limit):
        """Find actual users who learned skills and achieved something"""
        stories = []
        
        try:
            # Query profiles with skills and achievements
            profiles = db.collection('profiles').where('skills', '>', []).limit(50).stream()
            
            for profile_doc in profiles:
                profile_data = profile_doc.to_dict()
                profile_user_id = profile_doc.id
                
                # Skip self and non-eligible users
                if profile_user_id == user_id:
                    continue
                
                skills = profile_data.get('skills', [])
                if len(skills) < 1:
                    continue
                
                # Get gamification data to check achievements
                gami_doc = db.collection('gamification').document(profile_user_id).get()
                if not gami_doc.exists:
                    continue
                
                gami_data = gami_doc.to_dict()
                achievements = gami_data.get('achievements', [])
                points = gami_data.get('total_points', 0)
                
                # Check for applications/success
                apps_query = db.collection('applications').where('user_id', '==', profile_user_id).where('status', '==', 'accepted').limit(1).stream()
                has_success = len(list(apps_query)) > 0
                
                # Create story if user has shown growth
                if len(skills) >= 2 and (points >= 800 or has_success or len(achievements) >= 5):
                    story = self._create_story_from_profile(profile_data, gami_data, skills, has_success)
                    stories.append(story)
                    
                    if len(stories) >= limit:
                        break
        
        except Exception as e:
            print(f"Error finding real stories: {str(e)}")
        
        return stories
    
    def _create_story_from_profile(self, profile, gami_data, skills, has_success):
        """Create a success story from real user data"""
        # Get name from personal_info if nested, otherwise top level
        personal_info = profile.get('personal_info', {})
        name = personal_info.get('name', profile.get('name', 'A Student'))
        
        # Get college from education.institution
        education = profile.get('education', {})
        college = education.get('institution', 'a Tier 2/3 college')
        points = gami_data.get('total_points', 0)
        
        # Anonymize slightly
        first_name = name.split()[0] if name else 'Student'
        
        # Create achievement message
        if has_success:
            achievement = f"secured an internship"
        elif points >= 1500:
            achievement = f"reached {points} points and Level 5+"
        elif len(skills) >= 3:
            achievement = f"mastered {len(skills)} skills"
        else:
            achievement = f"gained {len(skills)} new skills and earned {points} points"
        
        # Time period (use points as proxy for time investment)
        months = max(2, min(12, points // 300))
        
        return {
            'id': profile.get('user_id', 'user_xxx'),
            'name': first_name,
            'college': college,
            'initial_state': f"started with basic knowledge in {skills[0]}",
            'skills_learned': skills[:3],  # Show top 3 skills
            'time_period': f"{months} months",
            'achievement': achievement,
            'points_earned': points,
            'key_action': f"Completed daily tasks consistently and applied to {max(5, points // 150)} opportunities",
            'is_real': True
        }
    
    def _get_synthetic_success_stories(self, limit):
        """Generate realistic synthetic success stories for inspiration"""
        
        synthetic_stories = [
            {
                'id': 'success_001',
                'name': 'Rahul',
                'college': 'Amity University',
                'initial_state': 'Started with basic Python knowledge, no internships',
                'skills_learned': ['Python', 'Machine Learning', 'Data Analysis'],
                'time_period': '6 months',
                'achievement': 'Secured ML internship at a startup',
                'points_earned': 1850,
                'key_action': 'Completed 3 ML projects, participated in 2 hackathons, maintained 30-day streak',
                'is_real': False
            },
            {
                'id': 'success_002',
                'name': 'Priya',
                'college': 'VIT Vellore',
                'initial_state': 'Third-year CSE student with no work experience',
                'skills_learned': ['React', 'Node.js', 'MongoDB'],
                'time_period': '4 months',
                'achievement': 'Built 2 full-stack projects, got freelance clients',
                'points_earned': 1620,
                'key_action': 'Used AI chatbot for personalized learning path, applied to 15+ opportunities',
                'is_real': False
            },
            {
                'id': 'success_003',
                'name': 'Arjun',
                'college': 'SRM Institute',
                'initial_state': 'Knew only Java from college, felt lost about career',
                'skills_learned': ['Spring Boot', 'AWS', 'Docker'],
                'time_period': '8 months',
                'achievement': 'Secured backend developer role at product company',
                'points_earned': 2340,
                'key_action': 'Leveraged eligibility checker, learned from rejections, improved resume 5 times',
                'is_real': False
            },
            {
                'id': 'success_004',
                'name': 'Sneha',
                'college': 'AKTU Affiliated College',
                'initial_state': 'Non-CS background (Electronics), wanted to switch to tech',
                'skills_learned': ['HTML/CSS', 'JavaScript', 'UI/UX Design'],
                'time_period': '10 months',
                'achievement': 'Landed frontend internship, built 4 live websites',
                'points_earned': 1980,
                'key_action': 'Started from scratch, completed every beginner task, joined 3 open-source projects',
                'is_real': False
            },
            {
                'id': 'success_005',
                'name': 'Karthik',
                'college': 'Lovely Professional University',
                'initial_state': 'Had programming basics but no real-world projects',
                'skills_learned': ['Django', 'PostgreSQL', 'REST APIs'],
                'time_period': '5 months',
                'achievement': 'Won college hackathon, got mentorship from alumni',
                'points_earned': 1550,
                'key_action': 'Focused on building one strong project per month, participated in challenges',
                'is_real': False
            },
            {
                'id': 'success_006',
                'name': 'Anjali',
                'college': 'Chitkara University',
                'initial_state': 'Good grades but zero practical skills',
                'skills_learned': ['Data Structures', 'Competitive Programming', 'Problem Solving'],
                'time_period': '7 months',
                'achievement': 'Cleared 3 technical interviews, got SDE internship offer',
                'points_earned': 2100,
                'key_action': 'Solved 200+ DSA problems, used AI for doubt clearing, maintained study streak',
                'is_real': False
            },
            {
                'id': 'success_007',
                'name': 'Vivek',
                'college': 'Jain University',
                'initial_state': "Wanted to get into AI but didn't know where to start",
                'skills_learned': ['Python', 'TensorFlow', 'NLP'],
                'time_period': '9 months',
                'achievement': 'Published research paper, secured research internship',
                'points_earned': 2250,
                'key_action': 'Followed AI learning roadmap from chatbot, joined study groups, read papers daily',
                'is_real': False
            },
            {
                'id': 'success_008',
                'name': 'Divya',
                'college': 'Graphic Era University',
                'initial_state': 'Introvert, no confidence in applying for opportunities',
                'skills_learned': ['Communication', 'Resume Building', 'Interview Skills'],
                'time_period': '3 months',
                'achievement': 'Applied to 25 opportunities, got 5 interview calls',
                'points_earned': 920,
                'key_action': 'Used eligibility score to identify realistic opportunities, improved profile weekly',
                'is_real': False
            }
        ]
        
        # Return random selection
        selected = random.sample(synthetic_stories, min(limit, len(synthetic_stories)))
        return selected
    
    def get_peer_growth_insights(self, user_id):
        """Get insights on how user can grow compared to peers - healthy competition"""
        try:
            db = self.firebase.db
            
            # Get user's current stats
            user_gami = db.collection('gamification').document(user_id).get()
            if not user_gami.exists:
                return {
                    'your_stats': {'points': 0, 'streak': 0, 'achievements': 0},
                    'peer_averages': {
                        'same_college': {'points': 500, 'streak': 5, 'achievements': 3},
                        'all_peers': {'points': 600, 'streak': 7, 'achievements': 4},
                        'total_peers': 100,
                        'college_peers': 15
                    },
                    'insights': [],
                    'recommendations': []
                }
            
            user_data = user_gami.to_dict()
            if not isinstance(user_data, dict):
                raise ValueError("Invalid user gamification data format")
                
            user_points = user_data.get('total_points', 0)
            user_streak = user_data.get('login_streak', 0)
            
            # Safely get achievements count
            achievements = user_data.get('achievements', [])
            if isinstance(achievements, list):
                user_achievements = len(achievements)
            else:
                user_achievements = 0
            
            # Get user profile for college
            user_profile = db.collection('profiles').document(user_id).get()
            if user_profile.exists:
                profile_data = user_profile.to_dict()
                education = profile_data.get('education', {})
                user_college = education.get('institution', 'Unknown')
            else:
                user_college = 'Unknown'
            
            # Get peer statistics
            peer_stats = self._get_peer_statistics(db, user_college)
            
            # Generate insights
            insights = self._generate_growth_insights(
                user_points, user_streak, user_achievements,
                peer_stats
            )
            
            return {
                'your_stats': {
                    'points': user_points,
                    'streak': user_streak,
                    'achievements': user_achievements
                },
                'peer_averages': peer_stats,
                'insights': insights,
                'recommendations': self._get_recommendations(user_data, peer_stats)
            }
        
        except Exception as e:
            print(f"Error getting peer insights: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return default data structure instead of error
            return {
                'your_stats': {'points': 0, 'streak': 0, 'achievements': 0},
                'peer_averages': {
                    'same_college': {'points': 500, 'streak': 5, 'achievements': 3},
                    'all_peers': {'points': 600, 'streak': 7, 'achievements': 4},
                    'total_peers': 100,
                    'college_peers': 15
                },
                'insights': [{
                    'type': 'overall',
                    'icon': '💪',
                    'message': 'Start your journey today!',
                    'motivation': 'Complete your first task to begin earning points.',
                    'status': 'growth_potential'
                }],
                'recommendations': [{
                    'priority': 'high',
                    'category': 'Getting Started',
                    'action': 'Complete your profile and take your first eligibility check',
                    'impact': 'Unlock personalized opportunities',
                    'time': '10 minutes'
                }]
            }
    
    def _get_peer_statistics(self, db, user_college):
        """Get average statistics from peers"""
        try:
            # Get all gamification data
            gami_docs = db.collection('gamification').stream()
            
            same_college_stats = []
            all_peers_stats = []
            
            for doc in gami_docs:
                data = doc.to_dict()
                points = data.get('total_points', 0)
                streak = data.get('login_streak', 0)
                achievements = len(data.get('achievements', []))
                
                all_peers_stats.append({
                    'points': points,
                    'streak': streak,
                    'achievements': achievements
                })
                
                # Check if same college
                profile = db.collection('profiles').document(doc.id).get()
                if profile.exists:
                    profile_data = profile.to_dict()
                    education = profile_data.get('education', {})
                    profile_college = education.get('institution', '')
                    if profile_college == user_college:
                        same_college_stats.append({
                            'points': points,
                            'streak': streak,
                            'achievements': achievements
                        })
            
            # Calculate averages
            def calc_avg(stats_list):
                if not stats_list:
                    return {'points': 0, 'streak': 0, 'achievements': 0}
                return {
                    'points': sum(s['points'] for s in stats_list) // len(stats_list),
                    'streak': sum(s['streak'] for s in stats_list) // len(stats_list),
                    'achievements': sum(s['achievements'] for s in stats_list) // len(stats_list)
                }
            
            return {
                'same_college': calc_avg(same_college_stats),
                'all_peers': calc_avg(all_peers_stats),
                'total_peers': len(all_peers_stats),
                'college_peers': len(same_college_stats)
            }
        
        except Exception as e:
            print(f"Error calculating peer stats: {str(e)}")
            return {
                'same_college': {'points': 500, 'streak': 5, 'achievements': 3},
                'all_peers': {'points': 600, 'streak': 7, 'achievements': 4},
                'total_peers': 100,
                'college_peers': 15
            }
    
    def _generate_growth_insights(self, user_points, user_streak, user_achievements, peer_stats):
        """Generate personalized insights for healthy competition"""
        insights = []
        
        same_college = peer_stats['same_college']
        all_peers = peer_stats['all_peers']
        
        # Points comparison
        if user_points < same_college['points']:
            diff = same_college['points'] - user_points
            insights.append({
                'type': 'points',
                'icon': '📈',
                'message': f"You're {diff} points behind your college average",
                'motivation': f"Complete 3 more daily tasks to catch up! ({diff // 30} days at current pace)",
                'status': 'behind'
            })
        elif user_points > same_college['points']:
            diff = user_points - same_college['points']
            insights.append({
                'type': 'points',
                'icon': '🏆',
                'message': f"You're {diff} points ahead of your college average!",
                'motivation': "Amazing! Keep this momentum going. You're inspiring others!",
                'status': 'ahead'
            })
        else:
            insights.append({
                'type': 'points',
                'icon': '🎯',
                'message': "You're at par with your college peers",
                'motivation': "Push a bit more to stand out! Just 100 more points will make a difference.",
                'status': 'equal'
            })
        
        # Streak comparison
        if user_streak < same_college['streak']:
            diff = same_college['streak'] - user_streak
            insights.append({
                'type': 'streak',
                'icon': '🔥',
                'message': f"Your peers have {diff} days longer streaks on average",
                'motivation': "Consistency wins! Log in daily for the next 7 days to build momentum.",
                'status': 'behind'
            })
        elif user_streak > same_college['streak']:
            insights.append({
                'type': 'streak',
                'icon': '⚡',
                'message': f"Your {user_streak}-day streak beats the college average!",
                'motivation': "You're the definition of consistent. Keep showing up!",
                'status': 'ahead'
            })
        
        # Achievements comparison
        if user_achievements < same_college['achievements']:
            diff = same_college['achievements'] - user_achievements
            insights.append({
                'type': 'achievements',
                'icon': '🎖️',
                'message': f"Earn {diff} more badges to match your peers",
                'motivation': "Focus on completing task sets and exploring new features to unlock more!",
                'status': 'behind'
            })
        elif user_achievements > same_college['achievements']:
            insights.append({
                'type': 'achievements',
                'icon': '🌟',
                'message': f"You've collected more achievements than most peers!",
                'motivation': "Badge collector! Your dedication shows.",
                'status': 'ahead'
            })
        
        # Overall standing
        total_user = user_points + (user_streak * 10) + (user_achievements * 50)
        total_peer = same_college['points'] + (same_college['streak'] * 10) + (same_college['achievements'] * 50)
        
        if total_user >= total_peer * 1.2:
            insights.append({
                'type': 'overall',
                'icon': '👑',
                'message': "You're in the TOP tier of your college!",
                'motivation': "Set an example for others. Share your journey!",
                'status': 'excellent'
            })
        elif total_user <= total_peer * 0.8:
            insights.append({
                'type': 'overall',
                'icon': '💪',
                'message': "You have room to grow - and that's exciting!",
                'motivation': "Small daily improvements = huge results over time. Start today!",
                'status': 'growth_potential'
            })
        
        return insights
    
    def _get_recommendations(self, user_data, peer_stats):
        """Get actionable recommendations for growth"""
        recommendations = []
        
        # Handle case where user_data might not be a dict
        if not isinstance(user_data, dict):
            return []
        
        user_points = user_data.get('total_points', 0)
        
        # Safely check daily tasks completion
        daily_tasks = user_data.get('daily_tasks', {})
        if isinstance(daily_tasks, dict):
            completed_tasks = len([k for k, v in daily_tasks.items() if isinstance(v, dict) and v.get('completed')])
        else:
            completed_tasks = 0
        
        # Task completion recommendation
        if completed_tasks < 3:
            recommendations.append({
                'priority': 'high',
                'category': 'Daily Tasks',
                'action': 'Complete at least 3 daily tasks today',
                'impact': '+90 points, build consistency',
                'time': '30-45 minutes'
            })
        
        # Application recommendation
        if user_points < peer_stats['all_peers']['points']:
            recommendations.append({
                'priority': 'high',
                'category': 'Opportunities',
                'action': 'Apply to 2 opportunities you\'re 70%+ eligible for',
                'impact': '+100 points + real-world experience',
                'time': '1-2 hours'
            })
        
        # Skill development
        recommendations.append({
            'priority': 'medium',
            'category': 'Skills',
            'action': 'Learn one new skill your peers are mastering',
            'impact': 'Unlock new opportunities, earn achievement badges',
            'time': '2-4 weeks (15 min/day)'
        })
        
        # Streak building
        recommendations.append({
            'priority': 'medium',
            'category': 'Consistency',
            'action': 'Maintain 7-day login streak',
            'impact': '+70 points, unlock streak achievement',
            'time': '5 min/day'
        })
        
        return recommendations[:3]  # Return top 3
