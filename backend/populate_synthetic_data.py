"""
Populate Firebase with Synthetic Data
Run this script to add realistic peer data to the database
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.firebase_service import FirebaseService
from services.synthetic_data_service import SyntheticDataService
from datetime import datetime
import random


def populate_synthetic_users(firebase_service, count=100):
    """Add synthetic users to gamification collection"""
    print(f"🔄 Generating {count} synthetic users...")
    users = SyntheticDataService.generate_peer_users(count)
    
    print(f"📝 Adding users to Firebase...")
    batch = firebase_service.db.batch()
    batch_count = 0
    
    for user in users:
        user_id = user['user_id']
        
        # Add to gamification collection
        gami_ref = firebase_service.db.collection('gamification').document(user_id)
        gami_data = {
            'user_id': user_id,
            'total_points': user['total_points'],
            'level': user['level'],
            'login_streak': user['login_streak'],
            'achievements': [],
            'actions': user['actions'],
            'last_login': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'is_synthetic': True
        }
        batch.set(gami_ref, gami_data)
        
        # Add to profiles collection (basic profile)
        profile_ref = firebase_service.db.collection('profiles').document(user_id)
        profile_data = {
            'user_id': user_id,
            'personal_info': {
                'name': user['name'],
                'email': f"{user_id}@example.com"
            },
            'education': {
                'degree': user['degree'],
                'major': user['major'],
                'institution': user['college'],
                'year': random.choice(['2024', '2025', '2026', '2027'])
            },
            'is_synthetic': True,
            'created_at': datetime.now().isoformat()
        }
        batch.set(profile_ref, profile_data)
        
        batch_count += 1
        
        # Firebase batch limit is 500, commit every 400
        if batch_count >= 400:
            print(f"  ✓ Committing batch of {batch_count} users...")
            batch.commit()
            batch = firebase_service.db.batch()
            batch_count = 0
    
    # Commit remaining
    if batch_count > 0:
        print(f"  ✓ Committing final batch of {batch_count} users...")
        batch.commit()
    
    print(f"✅ Successfully added {count} synthetic users!")
    return users


def populate_synthetic_applications(firebase_service, user_count=100, avg_apps=8):
    """Add synthetic applications for peer comparison"""
    print(f"\n🔄 Generating synthetic applications...")
    applications = SyntheticDataService.generate_peer_applications(user_count, avg_apps)
    
    print(f"📝 Adding {len(applications)} applications to Firebase...")
    batch = firebase_service.db.batch()
    batch_count = 0
    
    for i, app in enumerate(applications):
        app_id = f"synthetic_app_{i+1}"
        app_ref = firebase_service.db.collection('applications').document(app_id)
        
        app_data = {
            'user_id': app['user_id'],
            'opportunity_id': f"opp_{random.randint(1, 100)}",
            'opportunity_title': app['opportunity_title'],
            'category': app['category'],
            'status': app['status'],
            'eligibility_score': app['eligibility_score'],
            'created_at': app['created_at'],
            'updated_at': app['created_at'],
            'is_synthetic': True
        }
        
        batch.set(app_ref, app_data)
        batch_count += 1
        
        if batch_count >= 400:
            print(f"  ✓ Committing batch of {batch_count} applications...")
            batch.commit()
            batch = firebase_service.db.batch()
            batch_count = 0
    
    if batch_count > 0:
        print(f"  ✓ Committing final batch of {batch_count} applications...")
        batch.commit()
    
    print(f"✅ Successfully added {len(applications)} synthetic applications!")


def clear_synthetic_data(firebase_service):
    """Remove all synthetic data from database"""
    print("\n🗑️  Clearing existing synthetic data...")
    
    # Clear synthetic users from gamification
    gami_docs = firebase_service.db.collection('gamification')\
        .where('is_synthetic', '==', True).stream()
    
    batch = firebase_service.db.batch()
    count = 0
    for doc in gami_docs:
        batch.delete(doc.reference)
        count += 1
        if count >= 400:
            batch.commit()
            batch = firebase_service.db.batch()
            count = 0
    
    if count > 0:
        batch.commit()
    
    print(f"  ✓ Removed synthetic gamification data")
    
    # Clear synthetic profiles
    profile_docs = firebase_service.db.collection('profiles')\
        .where('is_synthetic', '==', True).stream()
    
    batch = firebase_service.db.batch()
    count = 0
    for doc in profile_docs:
        batch.delete(doc.reference)
        count += 1
        if count >= 400:
            batch.commit()
            batch = firebase_service.db.batch()
            count = 0
    
    if count > 0:
        batch.commit()
    
    print(f"  ✓ Removed synthetic profiles")
    
    # Clear synthetic applications
    app_docs = firebase_service.db.collection('applications')\
        .where('is_synthetic', '==', True).stream()
    
    batch = firebase_service.db.batch()
    count = 0
    for doc in app_docs:
        batch.delete(doc.reference)
        count += 1
        if count >= 400:
            batch.commit()
            batch = firebase_service.db.batch()
            count = 0
    
    if count > 0:
        batch.commit()
    
    print(f"  ✓ Removed synthetic applications")
    print("✅ Synthetic data cleared!")


def main():
    """Main function to populate synthetic data"""
    print("=" * 60)
    print("🚀 ORBIT - Synthetic Data Population Script")
    print("=" * 60)
    
    # Initialize Firebase
    print("\n🔧 Initializing Firebase...")
    firebase_service = FirebaseService()
    print("✅ Firebase connected!")
    
    # Ask user what to do
    print("\n📋 Options:")
    print("1. Add synthetic data (100 users + applications)")
    print("2. Clear all synthetic data")
    print("3. Replace synthetic data (clear + add)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Add data
        users = populate_synthetic_users(firebase_service, count=50)
        populate_synthetic_applications(firebase_service, user_count=50, avg_apps=8)
        print("\n" + "=" * 60)
        print("✨ Synthetic data added successfully!")
        print(f"📊 Total: 50 users with ~400 applications")
        print("=" * 60)
        
    elif choice == '2':
        # Clear data
        confirm = input("\n⚠️  Are you sure you want to clear all synthetic data? (yes/no): ")
        if confirm.lower() == 'yes':
            clear_synthetic_data(firebase_service)
        else:
            print("❌ Cancelled")
            
    elif choice == '3':
        # Replace data
        confirm = input("\n⚠️  This will clear and recreate synthetic data. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            clear_synthetic_data(firebase_service)
            users = populate_synthetic_users(firebase_service, count=100)
            populate_synthetic_applications(firebase_service, user_count=100, avg_apps=8)
            print("\n" + "=" * 60)
            print("✨ Synthetic data replaced successfully!")
            print(f"📊 Total: 100 users with ~800 applications")
            print(f"🎓 Colleges: Tier 2/3 (LPU, Amity, SRM, Regional, etc.)")
            print("=" * 60)
        else:
            print("❌ Cancelled")
    else:
        print("❌ Invalid choice")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
