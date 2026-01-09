# Sample Data for Testing

## Sample Student Profile

```json
{
  "education": {
    "degree": "B.Tech",
    "major": "Computer Science",
    "institution": "ABC Institute of Technology",
    "year": "3rd year",
    "cgpa_or_percentage": "8.5"
  },
  "skills": {
    "programming_languages": ["Python", "Java", "JavaScript"],
    "frameworks": ["React", "Django", "TensorFlow"],
    "tools": ["Git", "Docker", "VS Code"],
    "domains": ["Machine Learning", "Web Development", "Data Science"]
  },
  "experience": [
    {
      "type": "project",
      "title": "E-commerce Website",
      "organization": "Personal Project",
      "duration": "3 months",
      "description": "Built full-stack e-commerce platform using React and Django"
    },
    {
      "type": "internship",
      "title": "Software Development Intern",
      "organization": "TechCorp India",
      "duration": "Jun 2025 - Aug 2025",
      "description": "Worked on backend APIs and database optimization"
    }
  ],
  "achievements": [
    "Winner of college hackathon 2025",
    "Coursera Machine Learning Specialization"
  ],
  "interests": [
    "Artificial Intelligence",
    "Web Development",
    "Open Source"
  ],
  "self_description": "Passionate computer science student with strong interest in AI and web technologies. Love building practical solutions to real-world problems. Eager to learn and contribute to innovative projects."
}
```

## Sample Opportunity Criteria

### Example 1: AI Hackathon

**Title**: Smart India Hackathon 2026

**Eligibility Criteria**:
```
Open to undergraduate and postgraduate students enrolled in recognized institutions in India. 
Teams must consist of 6 members. All team members must be currently enrolled students. 
Prior hackathon experience is not required but basic programming knowledge is expected.
Students from all years and branches are welcome to participate.
```

**Expected Analysis**: Eligible (if student meets basic criteria)

---

### Example 2: ML Internship

**Title**: Google Summer of Code - ML Project

**Eligibility Criteria**:
```
Must be 18 years or older. Enrolled in or accepted into an accredited institution.
Strong programming skills in Python required. Prior experience with machine learning 
frameworks (TensorFlow, PyTorch, scikit-learn) is mandatory. Must have demonstrable 
ML projects on GitHub or similar platforms. Contributions to open-source ML projects 
are highly preferred.
```

**Expected Analysis**: Partially Eligible (if student lacks ML projects)

---

### Example 3: Senior Fellowship

**Title**: Microsoft Research Fellowship

**Eligibility Criteria**:
```
Open to final year undergraduate students and graduate students pursuing research in 
Computer Science. Minimum CGPA of 8.5 required. Must have published research papers 
or strong research project experience. Demonstrated leadership in technical communities. 
Prior research internship experience required.
```

**Expected Analysis**: Not Yet Eligible (if student lacks research experience)

---

## Sample Gemini Responses

### Response for "Partially Eligible" Case

```json
{
  "eligibility_status": "Partially Eligible",
  "reasons_met": [
    "Student is in 3rd year B.Tech Computer Science (meets education requirement)",
    "Has Python programming skills as required",
    "Shows interest in machine learning through coursework"
  ],
  "reasons_not_met": [
    "No demonstrable ML projects on GitHub mentioned",
    "Lacks hands-on experience with ML frameworks (TensorFlow, PyTorch)",
    "No evidence of prior work with machine learning models"
  ],
  "missing_skills": [
    "Practical experience with TensorFlow or PyTorch",
    "Model training and evaluation techniques",
    "ML project deployment experience"
  ],
  "missing_experience": [
    "Completed ML projects with documented results",
    "Kaggle competitions or ML challenges",
    "GitHub repository with ML code and explanations"
  ],
  "confidence_score": 65,
  "explanation_simple": "You have a solid foundation with your CS degree and Python skills, but this opportunity specifically wants to see hands-on ML project experience. The good news is that this gap is very achievable to fill in the next few weeks with focused effort.",
  "next_steps": [
    {
      "action": "Complete an end-to-end ML project (e.g., image classifier or sentiment analyzer)",
      "reason": "Demonstrates practical skills that directly match what the opportunity requires",
      "time_estimate": "2-3 weeks"
    },
    {
      "action": "Create a detailed GitHub repository for your project with README, code, and results",
      "reason": "Makes your work visible and shows you can document technical work professionally",
      "time_estimate": "1-2 days"
    },
    {
      "action": "Take a short online course on TensorFlow or PyTorch (Coursera, fast.ai)",
      "reason": "Fills the specific framework knowledge gap mentioned in requirements",
      "time_estimate": "2-3 weeks (can overlap with project)"
    },
    {
      "action": "Write a blog post or LinkedIn article explaining what you learned",
      "reason": "Shows communication skills and helps you reflect on your learning",
      "time_estimate": "2-3 hours"
    }
  ]
}
```

---

## Test Commands

### Test Backend Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Create profile
curl -X POST http://localhost:5000/api/profile/create \
  -H "Content-Type: application/json" \
  -d @sample_profile.json

# Search opportunities
curl -X POST http://localhost:5000/api/opportunities/search \
  -H "Content-Type: application/json" \
  -d '{"query": "AI hackathon", "opportunity_type": "hackathon"}'
```

---

## Demo Scenarios

### Scenario 1: Strong Match
- **Student**: 3rd year CS with multiple projects
- **Opportunity**: College hackathon (beginner-friendly)
- **Expected**: Green "Eligible" badge with encouragement

### Scenario 2: Growing Student
- **Student**: 2nd year CS, learning phase
- **Opportunity**: ML internship requiring experience
- **Expected**: Yellow "Partially Eligible" with specific roadmap

### Scenario 3: Early Journey
- **Student**: 1st year, just started coding
- **Opportunity**: Senior fellowship requiring research
- **Expected**: Red "Not Yet Eligible" but encouraging growth plan

---

## Mock Data Configuration

The application uses mock data when APIs aren't configured:

**Location**: `backend/services/opportunity_service.py`

**Method**: `_get_mock_search_results()`

You can customize mock opportunities for your demo by editing this function.

---

## Quick Fill Profile (For Demo)

Use this for rapid profile creation during demo:

```
Degree: B.Tech
Major: Computer Science
Institution: ABC Institute of Technology
Year: 3rd year
CGPA: 8.5

Programming Languages: Python, Java, JavaScript
Frameworks: React, Django
Tools: Git, Docker

Interests: Artificial Intelligence, Web Development

Description: Passionate CS student interested in AI and building practical solutions
```

---

This sample data helps you:
1. Test the system without waiting for AI
2. Prepare consistent demo scenarios
3. Understand expected outputs
4. Validate your setup
