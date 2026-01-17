"""
Analytics Service - User statistics, peer comparison, and insights with synthetic data
"""

from datetime import datetime, timedelta
from collections import defaultdict
from .synthetic_data_service import SyntheticDataService


class AnalyticsService:
    def __init__(self, firebase_service):
        """Initialize analytics service"""
        self.firebase = firebase_service
        self.db = firebase_service.db
    
    def get_user_analytics(self, user_id):
        """Get comprehensive analytics for user"""
        try:
            # Get user's applications
            apps = self.db.collection('applications')\
                .where('user_id', '==', user_id)\
                .stream()
            
            applications = [doc.to_dict() for doc in apps]
            
            # Get gamification data - initialize if doesn't exist
            gami_doc = self.db.collection('gamification').document(user_id).get()
            if gami_doc.exists:
                gami_data = gami_doc.to_dict()
            else:
                # Initialize empty gamification data for new users
                gami_data = {
                    'total_points': 0,
                    'level': 1,
                    'login_streak': 0,
                    'achievements': [],
                    'actions': {
                        'searches': 0,
                        'eligibility_checks': 0,
                        'tracker_saves': 0,
                        'applications': 0,
                        'chat_messages': 0,
                        'high_score_apps': 0,
                        'acceptances': 0
                    }
                }
            
            # Calculate statistics
            stats = self._calculate_statistics(applications, gami_data)
            
            # Get activity timeline
            timeline = self._get_activity_timeline(user_id, applications)
            
            # Get peer comparison
            peer_stats = self._get_peer_comparison(user_id, stats)
            
            return {
                'user_id': user_id,
                'statistics': stats,
                'timeline': timeline,
                'peer_comparison': peer_stats,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting analytics: {e}")
            import traceback
            traceback.print_exc()
            # Return empty analytics instead of None
            return {
                'user_id': user_id,
                'statistics': {
                    'total_applications': 0,
                    'pending': 0,
                    'under_review': 0,
                    'accepted': 0,
                    'rejected': 0,
                    'applications_7d': 0,
                    'applications_30d': 0,
                    'avg_eligibility_score': 0,
                    'acceptance_rate': 0,
                    'categories': {},
                    'monthly_trend': {},
                    'total_points': 0,
                    'level': 1,
                    'login_streak': 0,
                    'achievements_count': 0,
                    'searches': 0,
                    'eligibility_checks': 0
                },
                'timeline': [],
                'peer_comparison': None,
                'generated_at': datetime.now().isoformat()
            }
    
    def get_leaderboard_stats(self, user_id):
        """Get user's rank and surrounding users"""
        try:
            # Get all users sorted by points
            all_users = list(self.db.collection('gamification')\
                .order_by('total_points', direction='DESCENDING')\
                .stream())
            
            user_rank = None
            total_users = len(all_users)
            user_points = 0
            
            for rank, doc in enumerate(all_users, 1):
                if doc.id == user_id:
                    user_rank = rank
                    user_points = doc.to_dict()['total_points']
                    break
            
            # If user not found in leaderboard, they're at the bottom
            if not user_rank:
                user_rank = total_users + 1
                user_points = 0
            
            # Get surrounding users (3 above, 3 below)
            surrounding = self.db.collection('gamification')\
                .order_by('total_points', direction='DESCENDING')\
                .limit(user_rank + 3)\
                .stream()
            
            users_list = []
            for rank, doc in enumerate(surrounding, 1):
                if abs(rank - user_rank) <= 3:
                    data = doc.to_dict()
                    # Get profile name
                    try:
                        profile = self.db.collection('profiles').document(doc.id).get()
                        name = profile.to_dict().get('personal_info', {}).get('name', 'Anonymous')
                    except:
                        name = 'Anonymous'
                    
                    users_list.append({
                        'rank': rank,
                        'user_id': doc.id,
                        'name': name,
                        'points': data['total_points'],
                        'is_current_user': doc.id == user_id
                    })
            
            percentile = ((total_users - user_rank) / total_users) * 100 if total_users > 0 else 0
            
            return {
                'user_rank': user_rank,
                'total_users': total_users,
                'percentile': round(percentile, 1),
                'surrounding_users': users_list
            }
            
        except Exception as e:
            print(f"Error getting leaderboard stats: {e}")
            return None
    
    def get_insights(self, user_id):
        """Generate personalized insights and recommendations"""
        try:
            analytics = self.get_user_analytics(user_id)
            if not analytics:
                return []
            
            insights = []
            stats = analytics['statistics']
            
            # Application success rate
            if stats['total_applications'] > 0:
                success_rate = (stats['accepted'] / stats['total_applications']) * 100
                if success_rate > 50:
                    insights.append({
                        'type': 'success',
                        'icon': '🎉',
                        'message': f"Great job! {success_rate:.0f}% acceptance rate!",
                        'priority': 'high'
                    })
                elif success_rate < 20 and stats['total_applications'] > 5:
                    insights.append({
                        'type': 'warning',
                        'icon': '💡',
                        'message': "Consider refining your applications or targeting better-fit opportunities",
                        'priority': 'medium'
                    })
            
            # Activity level
            if stats.get('searches_7d', 0) < 3:
                insights.append({
                    'type': 'tip',
                    'icon': '🔍',
                    'message': "Search more opportunities to increase your chances!",
                    'priority': 'low'
                })
            
            # Application timing
            avg_response = stats.get('avg_response_time', 0)
            if avg_response > 14:
                insights.append({
                    'type': 'tip',
                    'icon': '⏰',
                    'message': "Apply faster! Average response time is over 2 weeks",
                    'priority': 'medium'
                })
            
            # Streak motivation
            streak = stats.get('login_streak', 0)
            if streak >= 7:
                insights.append({
                    'type': 'achievement',
                    'icon': '🔥',
                    'message': f"Amazing! {streak} day streak! Keep it up!",
                    'priority': 'high'
                })
            elif streak == 0:
                insights.append({
                    'type': 'tip',
                    'icon': '📅',
                    'message': "Visit daily to build your streak and earn bonus points!",
                    'priority': 'low'
                })
            
            # Peer comparison
            peer_stats = analytics['peer_comparison']
            if peer_stats:
                if peer_stats['percentile'] > 75:
                    insights.append({
                        'type': 'success',
                        'icon': '🏆',
                        'message': f"You're in the top {100 - peer_stats['percentile']:.0f}% of users!",
                        'priority': 'high'
                    })
            
            return insights
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return []
    
    def _calculate_statistics(self, applications, gami_data):
        """Calculate user statistics from applications and gamification data"""
        from datetime import timezone
        now = datetime.now(timezone.utc)
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)
        
        stats = {
            'total_applications': len(applications),
            'pending': 0,
            'under_review': 0,
            'accepted': 0,
            'rejected': 0,
            'applications_7d': 0,
            'applications_30d': 0,
            'avg_eligibility_score': 0,
            'categories': defaultdict(int),
            'monthly_trend': defaultdict(int)
        }
        
        total_score = 0
        
        for app in applications:
            status = app.get('status', 'pending').lower()
            stats[status] = stats.get(status, 0) + 1
            
            # Eligibility score
            score = app.get('eligibility_score', 0)
            if score:
                total_score += score
            
            # Time-based counts
            created_at_val = app.get('created_at', now.isoformat())
            # Handle both string and datetime/Timestamp objects
            if isinstance(created_at_val, str):
                created = datetime.fromisoformat(created_at_val.replace('Z', '+00:00'))
                # Make timezone-aware if naive
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            elif hasattr(created_at_val, 'isoformat'):
                created = created_at_val if isinstance(created_at_val, datetime) else created_at_val.to_pydatetime()
                # Make timezone-aware if naive
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            else:
                created = now
            
            if created >= seven_days_ago:
                stats['applications_7d'] += 1
            if created >= thirty_days_ago:
                stats['applications_30d'] += 1
            
            # Category tracking
            category = app.get('category', 'other')
            stats['categories'][category] += 1
            
            # Monthly trend
            month_key = created.strftime('%Y-%m')
            stats['monthly_trend'][month_key] += 1
        
        # Calculate averages
        if stats['total_applications'] > 0:
            stats['avg_eligibility_score'] = round(total_score / stats['total_applications'], 1)
            stats['acceptance_rate'] = round((stats['accepted'] / stats['total_applications']) * 100, 1)
        else:
            stats['acceptance_rate'] = 0
        
        # Add gamification stats
        stats['total_points'] = gami_data.get('total_points', 0)
        stats['level'] = gami_data.get('level', 1)
        stats['login_streak'] = gami_data.get('login_streak', 0)
        stats['achievements_count'] = len(gami_data.get('achievements', []))
        stats['searches'] = gami_data.get('actions', {}).get('searches', 0)
        stats['eligibility_checks'] = gami_data.get('actions', {}).get('eligibility_checks', 0)
        
        # Convert defaultdicts to regular dicts for JSON
        stats['categories'] = dict(stats['categories'])
        stats['monthly_trend'] = dict(stats['monthly_trend'])
        
        return stats
    
    def _get_activity_timeline(self, user_id, applications):
        """Generate activity timeline"""
        timeline = []
        
        # Add application events
        for app in applications:
            timeline.append({
                'type': 'application',
                'action': f"Applied to {app.get('opportunity_title', 'Unknown')}",
                'timestamp': app.get('created_at'),
                'icon': '📝',
                'status': app.get('status', 'pending')
            })
            
            # Add status updates
            updated = app.get('updated_at')
            if updated and updated != app.get('created_at'):
                timeline.append({
                    'type': 'status_update',
                    'action': f"Status updated: {app.get('status', 'Unknown')}",
                    'timestamp': updated,
                    'icon': '🔄',
                    'status': app.get('status', 'pending')
                })
        
        # Sort by timestamp - convert all timestamps to strings for comparison
        def normalize_timestamp(event):
            ts = event['timestamp']
            if hasattr(ts, 'isoformat'):
                return ts.isoformat()
            return str(ts)
        
        timeline.sort(key=normalize_timestamp, reverse=True)
        
        # Return last 20 events
        return timeline[:20]
    
    def _get_peer_comparison(self, user_id, user_stats):
        """Compare user statistics with real database peer data (including synthetic)"""
        try:
            # Get all users from database (real + synthetic)
            all_gami_docs = list(self.db.collection('gamification').stream())
            
            if len(all_gami_docs) < 2:
                # Fallback to synthetic generation if database is empty
                user_data = {
                    'user_id': user_id,
                    'total_points': user_stats.get('total_points', 0),
                    'level': user_stats.get('level', 1),
                    'login_streak': user_stats.get('login_streak', 0),
                    'actions': {
                        'searches': user_stats.get('searches', 0),
                        'eligibility_checks': user_stats.get('eligibility_checks', 0),
                        'tracker_saves': user_stats.get('tracker_saves', 0),
                        'applications': user_stats.get('applications', 0),
                        'chat_messages': user_stats.get('chat_messages', 0)
                    },
                    'total_applications': user_stats.get('total_applications', 0)
                }
                return SyntheticDataService.calculate_synthetic_peer_stats(user_data)
            
            # Use real database data
            all_users = []
            for doc in all_gami_docs:
                data = doc.to_dict()
                user_obj = {
                    'user_id': doc.id,
                    'name': 'Unknown',
                    'college': 'Unknown',
                    'total_points': data.get('total_points', 0),
                    'level': data.get('level', 1),
                    'login_streak': data.get('login_streak', 0),
                    'actions': data.get('actions', {}),
                    'achievements_count': len(data.get('achievements', [])),
                    'is_synthetic': data.get('is_synthetic', False)
                }
                
                # Get name and college from profile
                try:
                    profile_doc = self.db.collection('profiles').document(doc.id).get()
                    if profile_doc.exists:
                        profile = profile_doc.to_dict()
                        user_obj['name'] = profile.get('personal_info', {}).get('name', 'Unknown')
                        user_obj['college'] = profile.get('education', {}).get('institution', 'Unknown')
                except:
                    pass
                
                all_users.append(user_obj)
            
            # Sort by points
            all_users.sort(key=lambda x: x['total_points'], reverse=True)
            
            # Find user rank
            user_rank = next((i+1 for i, u in enumerate(all_users) 
                             if u['user_id'] == user_id), None)
            
            if not user_rank:
                user_rank = len(all_users) + 1
            
            # Calculate averages
            avg_points = sum(u['total_points'] for u in all_users) / len(all_users) if all_users else 0
            avg_streak = sum(u['login_streak'] for u in all_users) / len(all_users) if all_users else 0
            
            # Get application counts
            avg_applications = 0
            try:
                all_apps = list(self.db.collection('applications').stream())
                app_counts = {}
                for app in all_apps:
                    app_user_id = app.to_dict().get('user_id')
                    app_counts[app_user_id] = app_counts.get(app_user_id, 0) + 1
                
                if app_counts:
                    avg_applications = sum(app_counts.values()) / len(app_counts)
            except:
                pass
            
            # Calculate percentile
            users_below = sum(1 for u in all_users if u['total_points'] < user_stats.get('total_points', 0))
            percentile = (users_below / len(all_users)) * 100 if all_users else 0
            
            return {
                'total_users': len(all_users),
                'user_rank': user_rank,
                'percentile': round(percentile, 1),
                'avg_points': round(avg_points, 0),
                'your_points': user_stats.get('total_points', 0),
                'avg_applications': round(avg_applications, 1),
                'your_applications': user_stats.get('total_applications', 0),
                'avg_streak': round(avg_streak, 1),
                'your_streak': user_stats.get('login_streak', 0),
                'performance_vs_peers': 'above_average' if user_stats.get('total_points', 0) > avg_points else 'below_average',
                'top_users': [
                    {
                        'rank': i+1,
                        'name': u['name'],
                        'college': u.get('college', 'Unknown'),
                        'points': u['total_points'],
                        'level': u['level'],
                        'is_you': u['user_id'] == user_id
                    }
                    for i, u in enumerate(all_users[:10])
                ]
            }
            
        except Exception as e:
            print(f"Error calculating peer comparison: {e}")
            import traceback
            traceback.print_exc()
            return None
