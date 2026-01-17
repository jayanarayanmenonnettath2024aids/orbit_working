"""
Gamification Service - Points, badges, levels, achievements, and tasks
"""

from datetime import datetime, timedelta
import random


class GamificationService:
    def __init__(self, firebase_service):
        """Initialize gamification service"""
        self.firebase = firebase_service
        self.db = firebase_service.db
        
        # Points system - Enhanced with eligibility scoring
        self.POINT_VALUES = {
            'profile_complete': 100,
            'search_opportunity': 5,
            'check_eligibility': 10,
            'save_to_tracker': 15,
            'apply_submitted': 50,
            'status_update': 10,
            'chat_message': 2,
            'daily_login': 20,
            'streak_bonus': 10,  # Per day of streak
            'resume_upload': 50,
            'profile_update': 15,
            'high_eligibility_apply': 30,  # Bonus for applying with 80+ score
            'accepted_application': 100,  # Big bonus for acceptance
            'complete_task': 25,  # Task completion bonus
            'early_application': 20,  # Apply within 48h of discovery
            'referral': 50  # Refer a friend
        }
        
        # Level thresholds - More rewarding progression
        self.LEVELS = [
            {'level': 1, 'name': 'Fresher', 'min_points': 0, 'icon': '🌱', 'color': '#22c55e'},
            {'level': 2, 'name': 'Explorer', 'min_points': 100, 'icon': '🔍', 'color': '#3b82f6'},
            {'level': 3, 'name': 'Achiever', 'min_points': 300, 'icon': '⭐', 'color': '#8b5cf6'},
            {'level': 4, 'name': 'Expert', 'min_points': 600, 'icon': '🎯', 'color': '#f59e0b'},
            {'level': 5, 'name': 'Master', 'min_points': 1000, 'icon': '👑', 'color': '#eab308'},
            {'level': 6, 'name': 'Legend', 'min_points': 2000, 'icon': '🏆', 'color': '#ef4444'},
            {'level': 7, 'name': 'Champion', 'min_points': 3500, 'icon': '💎', 'color': '#06b6d4'}
        ]
        
        # Achievements/Badges - Enhanced with more variety
        self.ACHIEVEMENTS = {
            'first_search': {'name': 'First Steps', 'description': 'Searched your first opportunity', 'icon': '👣', 'points': 10, 'rarity': 'common'},
            'tracker_starter': {'name': 'Tracker Starter', 'description': 'Saved first opportunity to tracker', 'icon': '📌', 'points': 25, 'rarity': 'common'},
            'applicant': {'name': 'Applicant', 'description': 'Marked first application as submitted', 'icon': '📝', 'points': 50, 'rarity': 'common'},
            'consistent': {'name': 'Consistent Explorer', 'description': '7-day login streak', 'icon': '🔥', 'points': 100, 'rarity': 'uncommon'},
            'super_consistent': {'name': 'Dedicated Hunter', 'description': '30-day login streak', 'icon': '💪', 'points': 300, 'rarity': 'rare'},
            'ultra_consistent': {'name': 'Unstoppable', 'description': '90-day login streak', 'icon': '⚡', 'points': 500, 'rarity': 'epic'},
            'social': {'name': 'Chatty', 'description': 'Sent 50 chat messages', 'icon': '💬', 'points': 50, 'rarity': 'uncommon'},
            'organized': {'name': 'Organized Pro', 'description': 'Tracked 10 opportunities', 'icon': '📊', 'points': 100, 'rarity': 'uncommon'},
            'completionist': {'name': 'Profile Perfect', 'description': 'Completed 100% of profile', 'icon': '✨', 'points': 150, 'rarity': 'rare'},
            'early_bird': {'name': 'Early Bird', 'description': 'Applied within 24h of discovering', 'icon': '🐦', 'points': 75, 'rarity': 'uncommon'},
            'go_getter': {'name': 'Go-Getter', 'description': 'Applied to 5 opportunities', 'icon': '🚀', 'points': 200, 'rarity': 'rare'},
            'perfectionist': {'name': 'Perfectionist', 'description': 'Applied with 90+ eligibility score', 'icon': '💯', 'points': 150, 'rarity': 'rare'},
            'winner': {'name': 'Winner', 'description': 'Got 3 acceptances', 'icon': '🏅', 'points': 300, 'rarity': 'epic'},
            'champion': {'name': 'Champion', 'description': 'Applied to 20 opportunities', 'icon': '🎖️', 'points': 400, 'rarity': 'epic'},
            'scholar': {'name': 'Scholar', 'description': 'Got 5 scholarship acceptances', 'icon': '📚', 'points': 500, 'rarity': 'legendary'},
            'influencer': {'name': 'Influencer', 'description': 'Referred 5 friends', 'icon': '🌟', 'points': 250, 'rarity': 'epic'},
            'task_master': {'name': 'Task Master', 'description': 'Completed 20 tasks', 'icon': '✅', 'points': 200, 'rarity': 'rare'}
        }
        
        # Daily/Weekly Tasks for engagement
        self.TASKS = {
            'daily': [
                {'id': 'daily_search', 'title': 'Search 3 Opportunities', 'description': 'Find 3 new opportunities today', 'points': 15, 'target': 3, 'type': 'searches'},
                {'id': 'daily_eligibility', 'title': 'Check 2 Eligibility Scores', 'description': 'Check eligibility for 2 opportunities', 'points': 20, 'target': 2, 'type': 'eligibility_checks'},
                {'id': 'daily_chat', 'title': 'Chat with AI', 'description': 'Send 5 messages to AI chatbot', 'points': 10, 'target': 5, 'type': 'chat_messages'},
                {'id': 'daily_tracker', 'title': 'Save to Tracker', 'description': 'Add 1 opportunity to your tracker', 'points': 15, 'target': 1, 'type': 'tracker_saves'}
            ],
            'weekly': [
                {'id': 'weekly_apply', 'title': 'Submit 3 Applications', 'description': 'Apply to 3 opportunities this week', 'points': 100, 'target': 3, 'type': 'applications'},
                {'id': 'weekly_streak', 'title': 'Maintain Streak', 'description': 'Login 5 days this week', 'points': 75, 'target': 5, 'type': 'login_days'},
                {'id': 'weekly_high_score', 'title': 'Quality Applications', 'description': 'Apply with 80+ eligibility score twice', 'points': 80, 'target': 2, 'type': 'high_score_apps'},
                {'id': 'weekly_explorer', 'title': 'Diverse Explorer', 'description': 'Explore 3 different categories', 'points': 60, 'target': 3, 'type': 'categories_explored'}
            ]
        }
    
    def get_user_gamification(self, user_id):
        """Get complete gamification profile for user"""
        try:
            # Get or create gamification document
            gami_ref = self.db.collection('gamification').document(user_id)
            gami_doc = gami_ref.get()
            
            if not gami_doc.exists:
                # Initialize new user
                initial_data = {
                    'user_id': user_id,
                    'total_points': 0,
                    'level': 1,
                    'achievements': [],
                    'last_login': datetime.now().isoformat(),
                    'login_streak': 0,
                    'actions': {
                        'searches': 0,
                        'eligibility_checks': 0,
                        'tracker_saves': 0,
                        'applications': 0,
                        'chat_messages': 0,
                        'high_score_apps': 0,
                        'acceptances': 0
                    },
                    'daily_tasks': {},
                    'weekly_tasks': {},
                    'tasks_completed': 0,
                    'last_task_reset': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat()
                }
                gami_ref.set(initial_data)
                return self._calculate_gamification_status(initial_data, user_id)
            
            data = gami_doc.to_dict()
            
            # Reset tasks if needed
            self._check_and_reset_tasks(gami_ref, data)
            
            return self._calculate_gamification_status(data, user_id)
            
        except Exception as e:
            print(f"Error getting gamification: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def award_points(self, user_id, action, metadata=None):
        """Award points for user action and check for level-ups/achievements"""
        try:
            gami_ref = self.db.collection('gamification').document(user_id)
            gami_doc = gami_ref.get()
            
            if not gami_doc.exists:
                # Initialize if doesn't exist
                self.get_user_gamification(user_id)
                gami_doc = gami_ref.get()
            
            data = gami_doc.to_dict()
            
            # Base points
            points = self.POINT_VALUES.get(action, 0)
            
            # Bonus points for high eligibility score applications
            if action == 'apply_submitted' and metadata:
                eligibility_score = metadata.get('eligibility_score', 0)
                if eligibility_score >= 80:
                    points += self.POINT_VALUES['high_eligibility_apply']
                    data['actions']['high_score_apps'] = data.get('actions', {}).get('high_score_apps', 0) + 1
            
            # Bonus for accepted applications
            if action == 'status_update' and metadata:
                if metadata.get('status') == 'accepted':
                    points += self.POINT_VALUES['accepted_application']
                    data['actions']['acceptances'] = data.get('actions', {}).get('acceptances', 0) + 1
            
            old_points = data['total_points']
            new_points = old_points + points
            
            # Update action counter
            action_map = {
                'search_opportunity': 'searches',
                'check_eligibility': 'eligibility_checks',
                'save_to_tracker': 'tracker_saves',
                'apply_submitted': 'applications',
                'chat_message': 'chat_messages'
            }
            
            if action in action_map:
                counter_key = action_map[action]
                data['actions'][counter_key] = data.get('actions', {}).get(counter_key, 0) + 1
            
            # Check and update tasks
            task_completed = self._check_and_update_tasks(data, action, metadata)
            
            # Check for level up
            old_level = self._get_level_from_points(old_points)
            new_level = self._get_level_from_points(new_points)
            leveled_up = new_level['level'] > old_level['level']
            
            # Check for new achievements
            new_achievements = self._check_achievements(data, action, metadata)
            
            # Update database
            update_data = {
                'total_points': new_points,
                'level': new_level['level'],
                'actions': data['actions'],
                'achievements': data.get('achievements', []) + new_achievements,
                'updated_at': datetime.now().isoformat()
            }
            
            if task_completed:
                update_data['daily_tasks'] = data.get('daily_tasks', {})
                update_data['weekly_tasks'] = data.get('weekly_tasks', {})
                update_data['tasks_completed'] = data.get('tasks_completed', 0)
            
            gami_ref.update(update_data)
            
            return {
                'success': True,
                'points_awarded': points,
                'new_total': new_points,
                'leveled_up': leveled_up,
                'new_level': new_level if leveled_up else None,
                'new_achievements': [self.ACHIEVEMENTS[a] for a in new_achievements],
                'task_completed': task_completed
            }
            
        except Exception as e:
            print(f"Error awarding points: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_login_streak(self, user_id):
        """Update daily login streak"""
        try:
            gami_ref = self.db.collection('gamification').document(user_id)
            gami_doc = gami_ref.get()
            
            if not gami_doc.exists:
                return self.award_points(user_id, 'daily_login')
            
            data = gami_doc.to_dict()
            last_login = datetime.fromisoformat(data.get('last_login', datetime.now().isoformat()))
            now = datetime.now()
            
            # Check if last login was yesterday
            days_diff = (now.date() - last_login.date()).days
            
            if days_diff == 1:
                # Continue streak
                new_streak = data.get('login_streak', 0) + 1
                bonus_points = self.POINT_VALUES['daily_login'] + (new_streak * self.POINT_VALUES['streak_bonus'])
            elif days_diff == 0:
                # Same day, no change
                return {'success': True, 'message': 'Already logged in today'}
            else:
                # Streak broken, restart
                new_streak = 1
                bonus_points = self.POINT_VALUES['daily_login']
            
            gami_ref.update({
                'last_login': now.isoformat(),
                'login_streak': new_streak,
                'total_points': data['total_points'] + bonus_points
            })
            
            return {
                'success': True,
                'streak': new_streak,
                'points_awarded': bonus_points
            }
            
        except Exception as e:
            print(f"Error updating streak: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_leaderboard(self, limit=50):
        """Get top users by points"""
        try:
            users = self.db.collection('gamification')\
                .order_by('total_points', direction='DESCENDING')\
                .limit(limit)\
                .stream()
            
            leaderboard = []
            for rank, doc in enumerate(users, 1):
                data = doc.to_dict()
                user_id = data['user_id']
                
                # Get user profile name
                try:
                    profile = self.db.collection('profiles').document(user_id).get()
                    name = profile.to_dict().get('personal_info', {}).get('name', 'Anonymous User')
                except:
                    name = 'Anonymous User'
                
                level_info = self._get_level_from_points(data['total_points'])
                
                leaderboard.append({
                    'rank': rank,
                    'user_id': user_id,
                    'name': name,
                    'points': data['total_points'],
                    'level': level_info['level'],
                    'level_name': level_info['name'],
                    'level_icon': level_info['icon'],
                    'achievements_count': len(data.get('achievements', [])),
                    'login_streak': data.get('login_streak', 0)
                })
            
            return leaderboard
            
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []
    
    def get_leaderboard_with_user(self, top_limit=10, user_id=None):
        """Get top N users + current user if not in top N"""
        try:
            # Get all users sorted by points to calculate accurate ranks
            all_users = self.db.collection('gamification')\
                .order_by('total_points', direction='DESCENDING')\
                .stream()
            
            leaderboard = []
            user_entry = None
            user_rank = None
            
            for rank, doc in enumerate(all_users, 1):
                data = doc.to_dict()
                current_user_id = data['user_id']
                
                # Get user profile name
                try:
                    profile = self.db.collection('profiles').document(current_user_id).get()
                    name = profile.to_dict().get('personal_info', {}).get('name', 'Anonymous User')
                except:
                    name = 'Anonymous User'
                
                level_info = self._get_level_from_points(data['total_points'])
                
                entry = {
                    'rank': rank,
                    'user_id': current_user_id,
                    'name': name,
                    'points': data['total_points'],
                    'level': level_info['level'],
                    'level_name': level_info['name'],
                    'level_icon': level_info['icon'],
                    'achievements_count': len(data.get('achievements', [])),
                    'login_streak': data.get('login_streak', 0)
                }
                
                # Add to top N
                if rank <= top_limit:
                    leaderboard.append(entry)
                
                # Track current user's position
                if user_id and current_user_id == user_id:
                    user_entry = entry
                    user_rank = rank
            
            # If user is not in top N, add them at the end
            if user_id and user_rank and user_rank > top_limit and user_entry:
                leaderboard.append(user_entry)
            
            return {
                'leaderboard': leaderboard,
                'user_rank': user_rank,
                'total_users': rank if 'rank' in locals() else 0,
                'show_separator': user_rank and user_rank > top_limit
            }
            
        except Exception as e:
            print(f"Error getting leaderboard with user: {e}")
            return {'leaderboard': [], 'user_rank': None, 'total_users': 0, 'show_separator': False}
    
    def _calculate_gamification_status(self, data, user_id):
        """Calculate current level, progress, achievements, and tasks"""
        points = data['total_points']
        level_info = self._get_level_from_points(points)
        
        # Calculate progress to next level
        next_level_idx = level_info['level']
        if next_level_idx < len(self.LEVELS):
            next_level = self.LEVELS[next_level_idx]
            progress = ((points - level_info['min_points']) / 
                       (next_level['min_points'] - level_info['min_points'])) * 100
        else:
            next_level = None
            progress = 100
        
        # Get achievement details with rarity
        earned_achievements = []
        for a in data.get('achievements', []):
            # Handle both dict format {'id': 'xxx'} and string format 'xxx'
            achievement_id = a.get('id') if isinstance(a, dict) else a
            
            if achievement_id in self.ACHIEVEMENTS:
                achievement_data = self.ACHIEVEMENTS[achievement_id].copy()
                achievement_data['id'] = achievement_id
                
                # Add earned_at timestamp if available
                if isinstance(a, dict) and 'earned_at' in a:
                    achievement_data['earned_at'] = a['earned_at']
                
                earned_achievements.append(achievement_data)
        
        # Get active tasks with progress
        daily_tasks = self._get_task_progress(data, 'daily')
        weekly_tasks = self._get_task_progress(data, 'weekly')
        
        return {
            'user_id': data['user_id'],
            'total_points': points,
            'level': level_info['level'],
            'level_name': level_info['name'],
            'level_icon': level_info['icon'],
            'level_color': level_info.get('color', '#6366f1'),
            'progress_to_next': round(progress, 1),
            'next_level': next_level,
            'achievements': earned_achievements,
            'achievements_count': len(earned_achievements),
            'login_streak': data.get('login_streak', 0),
            'actions': data.get('actions', {}),
            'daily_tasks': daily_tasks,
            'weekly_tasks': weekly_tasks,
            'tasks_completed_total': data.get('tasks_completed', 0)
        }
    
    def _get_level_from_points(self, points):
        """Get level information from points"""
        for i in range(len(self.LEVELS) - 1, -1, -1):
            if points >= self.LEVELS[i]['min_points']:
                return self.LEVELS[i]
        return self.LEVELS[0]
    
    def _check_achievements(self, data, action, metadata):
        """Check if action unlocks new achievements"""
        new_achievements = []
        current_achievements = data.get('achievements', [])
        actions = data.get('actions', {})
        
        # First search
        if action == 'search_opportunity' and actions.get('searches', 0) == 1:
            if 'first_search' not in current_achievements:
                new_achievements.append('first_search')
        
        # First tracker save
        if action == 'save_to_tracker' and actions.get('tracker_saves', 0) == 1:
            if 'tracker_starter' not in current_achievements:
                new_achievements.append('tracker_starter')
        
        # First application
        if action == 'apply_submitted' and actions.get('applications', 0) == 1:
            if 'applicant' not in current_achievements:
                new_achievements.append('applicant')
        
        # Streak achievements
        streak = data.get('login_streak', 0)
        if streak >= 7 and 'consistent' not in current_achievements:
            new_achievements.append('consistent')
        if streak >= 30 and 'super_consistent' not in current_achievements:
            new_achievements.append('super_consistent')
        if streak >= 90 and 'ultra_consistent' not in current_achievements:
            new_achievements.append('ultra_consistent')
        
        # Chat messages
        if actions.get('chat_messages', 0) >= 50 and 'social' not in current_achievements:
            new_achievements.append('social')
        
        # Tracked opportunities
        if actions.get('tracker_saves', 0) >= 10 and 'organized' not in current_achievements:
            new_achievements.append('organized')
        
        # Application milestones
        app_count = actions.get('applications', 0)
        if app_count >= 5 and 'go_getter' not in current_achievements:
            new_achievements.append('go_getter')
        if app_count >= 20 and 'champion' not in current_achievements:
            new_achievements.append('champion')
        
        # High eligibility application
        if action == 'apply_submitted' and metadata:
            if metadata.get('eligibility_score', 0) >= 90:
                if 'perfectionist' not in current_achievements:
                    new_achievements.append('perfectionist')
        
        # Acceptances
        acceptances = actions.get('acceptances', 0)
        if acceptances >= 3 and 'winner' not in current_achievements:
            new_achievements.append('winner')
        
        # Tasks
        tasks_completed = data.get('tasks_completed', 0)
        if tasks_completed >= 20 and 'task_master' not in current_achievements:
            new_achievements.append('task_master')
        
        return new_achievements
    
    def _check_and_reset_tasks(self, gami_ref, data):
        """Check if tasks need to be reset (daily/weekly)"""
        now = datetime.now()
        last_reset = datetime.fromisoformat(data.get('last_task_reset', now.isoformat()))
        
        # Reset daily tasks at midnight
        if now.date() > last_reset.date():
            data['daily_tasks'] = {}
            gami_ref.update({
                'daily_tasks': {},
                'last_task_reset': now.isoformat()
            })
        
        # Reset weekly tasks on Monday
        if now.isocalendar()[1] != last_reset.isocalendar()[1]:
            data['weekly_tasks'] = {}
            gami_ref.update({'weekly_tasks': {}})
    
    def _check_and_update_tasks(self, data, action, metadata):
        """Check if action completes any tasks"""
        task_completed = False
        
        # Map actions to task types
        action_to_type = {
            'search_opportunity': 'searches',
            'check_eligibility': 'eligibility_checks',
            'chat_message': 'chat_messages',
            'save_to_tracker': 'tracker_saves',
            'apply_submitted': 'applications'
        }
        
        task_type = action_to_type.get(action)
        if not task_type:
            return False
        
        # Check daily tasks
        for task in self.TASKS['daily']:
            if task['type'] == task_type:
                task_id = task['id']
                current = data.get('daily_tasks', {}).get(task_id, {}).get('progress', 0)
                new_progress = current + 1
                
                if 'daily_tasks' not in data:
                    data['daily_tasks'] = {}
                
                data['daily_tasks'][task_id] = {
                    'progress': new_progress,
                    'completed': new_progress >= task['target']
                }
                
                if new_progress == task['target']:
                    data['total_points'] = data.get('total_points', 0) + task['points']
                    data['tasks_completed'] = data.get('tasks_completed', 0) + 1
                    task_completed = True
        
        # Check weekly tasks
        for task in self.TASKS['weekly']:
            if task['type'] == task_type:
                task_id = task['id']
                current = data.get('weekly_tasks', {}).get(task_id, {}).get('progress', 0)
                new_progress = current + 1
                
                # Special handling for high score apps
                if task_type == 'applications' and metadata:
                    if task['id'] == 'weekly_high_score':
                        if metadata.get('eligibility_score', 0) >= 80:
                            new_progress = current + 1
                        else:
                            continue
                
                if 'weekly_tasks' not in data:
                    data['weekly_tasks'] = {}
                
                data['weekly_tasks'][task_id] = {
                    'progress': new_progress,
                    'completed': new_progress >= task['target']
                }
                
                if new_progress == task['target']:
                    data['total_points'] = data.get('total_points', 0) + task['points']
                    data['tasks_completed'] = data.get('tasks_completed', 0) + 1
                    task_completed = True
        
        return task_completed
    
    def _get_task_progress(self, data, task_period):
        """Get tasks with current progress"""
        tasks = self.TASKS[task_period]
        task_data = data.get(f'{task_period}_tasks', {})
        
        result = []
        for task in tasks:
            task_id = task['id']
            progress = task_data.get(task_id, {}).get('progress', 0)
            completed = task_data.get(task_id, {}).get('completed', False)
            
            result.append({
                **task,
                'progress': progress,
                'completed': completed,
                'percentage': min(100, (progress / task['target']) * 100)
            })
        
        return result
