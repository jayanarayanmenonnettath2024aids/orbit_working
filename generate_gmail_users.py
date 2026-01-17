"""
Generate 50 Realistic Synthetic Users with Gmail Addresses
Each user has: email, password, profile, gamification stats, applications
"""
import sys
sys.path.insert(0, r'C:\Users\JAYAN\Downloads\orbit\backend')

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import random
import hashlib

# Initialize
cred = credentials.Certificate(r'C:\Users\JAYAN\Downloads\orbit\backend\firebase-credentials.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Indian names for realistic emails
INDIAN_NAMES = [
    ('Aarav', 'Sharma'), ('Priya', 'Nair'), ('Rohan', 'Patel'), ('Ananya', 'Gupta'),
    ('Arjun', 'Kumar'), ('Diya', 'Singh'), ('Vihaan', 'Verma'), ('Isha', 'Reddy'),
    ('Aditya', 'Mehta'), ('Sai', 'Iyer'), ('Dhruv', 'Joshi'), ('Neha', 'Sharma'),
    ('Kabir', 'Khan'), ('Riya', 'Das'), ('Ved', 'Mishra'), ('Kiara', 'Malhotra'),
    ('Atharv', 'Rao'), ('Saanvi', 'Jain'), ('Ayaan', 'Pandey'), ('Navya', 'Desai'),
    ('Reyansh', 'Kapoor'), ('Myra', 'Bhat'), ('Krishna', 'Pillai'), ('Aanya', 'Menon'),
    ('Vivaan', 'Agarwal'), ('Sara', 'Chaudhary'), ('Shivansh', 'Sinha'), ('Avni', 'Kulkarni'),
    ('Om', 'Bhatt'), ('Anika', 'Banerjee'), ('Aryan', 'Thakur'), ('Mira', 'Saxena'),
    ('Ishaan', 'Ghosh'), ('Pari', 'Mukherjee'), ('Rudra', 'Dutta'), ('Devi', 'Chopra'),
    ('Kian', 'Trivedi'), ('Aditi', 'Shetty'), ('Arnav', 'Tiwari'), ('Tanvi', 'Kohli'),
    ('Yash', 'Bajaj'), ('Shreya', 'Naik'), ('Pranav', 'Arora'), ('Roshni', 'Bose'),
    ('Aarush', 'Goswami'), ('Kavya', 'Varma'), ('Laksh', 'Choudhury'), ('Aadhya', 'Yadav'),
    ('Dev', 'Dubey'), ('Anvi', 'Pathak'), ('Shaurya', 'Bhattacharya'), ('Ishika', 'Nanda'),
    ('Vedant', 'Chatterjee'), ('Reet', 'Saini'), ('Advait', 'Kaur'), ('Samaira', 'Gill'),
    ('Shivin', 'Dhawan'), ('Larisa', 'Oberoi'), ('Ayush', 'Sethi'), ('Nisha', 'Batra'),
    ('Raghav', 'Mittal'), ('Trisha', 'Sen'), ('Veer', 'Rana'), ('Pooja', 'Hegde'),
    ('Siddharth', 'Roy'), ('Meera', 'Deshpande'), ('Neil', 'Pawar'), ('Rhea', 'Shukla'),
    ('Karthik', 'Nambiar'), ('Simran', 'Garg'), ('Raj', 'Balakrishnan'), ('Aarohi', 'Misra'),
    ('Advay', 'Bansal'), ('Ira', 'Jha'), ('Kabir', 'Kamat'), ('Navya', 'Vohra'),
    ('Ranveer', 'Singhal'), ('Kiara', 'Dalal'), ('Arhaan', 'Bhardwaj'), ('Diya', 'Rawal'),
    ('Shlok', 'Kashyap'), ('Anisha', 'Rathore'), ('Ayaan', 'Dhillon'), ('Tanisha', 'Sood'),
    ('Vivaan', 'Khanna'), ('Myra', 'Bakshi'), ('Aarav', 'Chauhan'), ('Saanvi', 'Malik'),
    ('Dhruv', 'Tandon'), ('Aadhya', 'Goel'), ('Shivansh', 'Ahluwalia'), ('Pari', 'Rastogi'),
    ('Reyansh', 'Mahajan'), ('Aanya', 'Sahni'), ('Om', 'Vyas'), ('Riya', 'Suresh'),
    ('Aryan', 'Srivastava'), ('Diya', 'Venkatesh'), ('Krishna', 'Shankar'), ('Priya', 'Natarajan')
]

TIER_2_3_COLLEGES = [
    'Lovely Professional University', 'Amity University', 'SRM University',
    'VIT Vellore', 'Manipal Institute', 'Chitkara University',
    'Chandigarh University', 'Thapar Institute', 'BITS Pilani Hyderabad',
    'LPU Phagwara', 'Jaipur Engineering College', 'Poornima University',
    'Arya College', 'Galgotias University', 'GL Bajaj', 'JECRC University',
    'Sharda University', 'AKTU Lucknow', 'PTU Jalandhar', 'RTU Kota',
    'Mumbai University', 'Delhi University', 'Bangalore University',
    'Pune University', 'Anna University', 'Jadavpur University'
]

DEGREES = ['B.Tech', 'B.E', 'MCA', 'M.Tech', 'BCA']
MAJORS = ['Computer Science', 'Information Technology', 'Electronics', 'Mechanical', 'Civil', 'AI/ML']
CATEGORIES = ['hackathon', 'internship', 'fellowship', 'competition', 'scholarship']

def generate_password(first_name, last_name, index):
    """Generate unique but predictable password for each user"""
    # Format: FirstnameLastname@123 (e.g., AaravSharma@123)
    return f"{first_name}{last_name}@{100 + index}"

def generate_email(first_name, last_name, index):
    """Generate Gmail address"""
    # Format: firstname.lastname.XX@gmail.com
    return f"{first_name.lower()}.{last_name.lower()}.{index+1}@gmail.com"

print("=" * 70)
print("🚀 ORBIT - New Synthetic Data Generation with Gmail Addresses")
print("=" * 70)

print("\n📧 Generating 50 users with real Gmail addresses...")

created_users = 0
created_profiles = 0
created_gami = 0
created_apps = 0

credentials_list = []

for i in range(50):
    first_name, last_name = INDIAN_NAMES[i]
    email = generate_email(first_name, last_name, i)
    password = generate_password(first_name, last_name, i)
    user_id = f"user_{i+1:03d}"  # user_001, user_002, etc.
    
    # Save credentials for output
    credentials_list.append({'email': email, 'password': password, 'name': f"{first_name} {last_name}"})
    
    try:
        # 1. Create AUTH account in 'users' collection
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'user_id': user_id,
            'name': f"{first_name} {last_name}",
            'created_at': datetime.now().isoformat(),
            'is_synthetic': True,
            'auth_provider': 'local'
        }
        db.collection('users').document(user_id).set(user_data)
        created_users += 1
        
        # 2. Create PROFILE
        profile_data = {
            'user_id': user_id,
            'personal_info': {
                'name': f"{first_name} {last_name}",
                'email': email
            },
            'education': {
                'degree': random.choice(DEGREES),
                'major': random.choice(MAJORS),
                'institution': random.choice(TIER_2_3_COLLEGES),
                'year': random.choice(['2024', '2025', '2026', '2027'])
            },
            'is_synthetic': True,
            'created_at': datetime.now().isoformat()
        }
        db.collection('profiles').document(user_id).set(profile_data)
        created_profiles += 1
        
        # 3. Create GAMIFICATION stats
        # Realistic point distribution
        point_rand = random.random()
        if point_rand < 0.6:  # 60% have low points (50-500)
            points = random.randint(50, 500)
            level = random.randint(1, 2)
        elif point_rand < 0.9:  # 30% have moderate points (500-1500)
            points = random.randint(500, 1500)
            level = random.randint(2, 4)
        else:  # 10% have high points (1500-2500)
            points = random.randint(1500, 2500)
            level = random.randint(4, 6)
        
        # Streak distribution
        streak_rand = random.random()
        if streak_rand < 0.7:  # 70% have 1-3 days
            streak = random.randint(1, 3)
        elif streak_rand < 0.9:  # 20% have 4-10 days
            streak = random.randint(4, 10)
        else:  # 10% have 11+ days
            streak = random.randint(11, 45)
        
        # Activity-based actions
        searches = int(points / 15) + random.randint(0, 10)
        eligibility_checks = int(points / 20) + random.randint(0, 8)
        tracker_saves = int(points / 15) + random.randint(0, 5)
        applications = int(points / 100) + random.randint(0, 3)
        chat_messages = random.randint(5, 50)
        
        # Achievements based on activity
        achievement_count = min(10, int(points / 300) + random.randint(0, 3))
        possible_achievements = [
            'first_search', 'first_application', 'tracker_starter', 'applicant',
            'consistent', 'early_bird', 'organized', 'social',
            'completionist', 'go_getter', 'perfectionist', 'task_master',
            'winner', 'champion', 'influencer', 'ultra_consistent', 'scholar'
        ]
        achievements = []
        for j in range(min(achievement_count, len(possible_achievements))):
            achievements.append({
                'id': possible_achievements[j],
                'earned_at': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            })
        
        gami_data = {
            'user_id': user_id,
            'total_points': points,
            'level': level,
            'login_streak': streak,
            'achievements': achievements,
            'actions': {
                'searches': searches,
                'eligibility_checks': eligibility_checks,
                'tracker_saves': tracker_saves,
                'applications': applications,
                'chat_messages': chat_messages,
                'high_score_apps': max(0, applications - 1),
                'acceptances': min(2, max(0, applications - 2))
            },
            'last_login': datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'is_synthetic': True,
            'daily_tasks': {},
            'weekly_tasks': {},
            'tasks_completed': 0,
            'last_task_reset': datetime.now().isoformat()
        }
        db.collection('gamification').document(user_id).set(gami_data)
        created_gami += 1
        
        # 4. Create APPLICATIONS (realistic number)
        num_apps = max(0, int(applications))
        for j in range(num_apps):
            status_rand = random.random()
            if status_rand < 0.4:
                status = 'pending'
            elif status_rand < 0.6:
                status = 'under_review'
            elif status_rand < 0.75:
                status = 'accepted'
            else:
                status = 'rejected'
            
            score_rand = random.random()
            if score_rand < 0.7:
                eligibility_score = random.randint(60, 85)
            elif score_rand < 0.85:
                eligibility_score = random.randint(40, 60)
            else:
                eligibility_score = random.randint(85, 95)
            
            days_ago = random.randint(1, 180)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            app_data = {
                'user_id': user_id,
                'opportunity_title': f"{random.choice(['Tech', 'AI', 'Web', 'ML', 'Data'])} {random.choice(['Hackathon', 'Internship', 'Fellowship', 'Competition'])} {random.randint(2025, 2026)}",
                'category': random.choice(CATEGORIES),
                'status': status,
                'eligibility_score': eligibility_score,
                'created_at': created_at.isoformat(),
                'is_synthetic': True
            }
            db.collection('applications').add(app_data)
            created_apps += 1
        
        if (i + 1) % 20 == 0:
            print(f"  ✓ Generated {i+1} users...")
            
    except Exception as e:
        print(f"  ⚠️  Error creating user {i+1}: {e}")

print(f"\n✅ Created {created_users} user accounts")
print(f"✅ Created {created_profiles} profiles")
print(f"✅ Created {created_gami} gamification records")
print(f"✅ Created {created_apps} applications")

# Save credentials to file
print("\n📝 Saving login credentials...")
with open('synthetic_credentials.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("ORBIT - Synthetic User Login Credentials\n")
    f.write("=" * 70 + "\n\n")
    for idx, cred in enumerate(credentials_list, 1):
        f.write(f"{idx}. {cred['name']}\n")
        f.write(f"   Email: {cred['email']}\n")
        f.write(f"   Password: {cred['password']}\n\n")

print(f"✅ Credentials saved to 'synthetic_credentials.txt'")

print("\n" + "=" * 70)
print("✨ Sample Login Credentials:")
print("=" * 70)
for i in range(min(5, len(credentials_list))):
    cred = credentials_list[i]
    print(f"{i+1}. {cred['name']}")
    print(f"   Email: {cred['email']}")
    print(f"   Password: {cred['password']}\n")

print("=" * 70)
print("✅ All 100 users generated successfully!")
print("📄 Full credentials list saved to: synthetic_credentials.txt")
print("=" * 70)
