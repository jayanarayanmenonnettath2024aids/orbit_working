# 🎯 AI-Powered Opportunity Intelligence & Guidance System

**"Never just say 'Not Eligible' — Always explain why and guide how to improve"**

---

## 🚀 Project Overview

This is a **reasoning + explanation + guidance engine** built for students in underserved campuses across India. Unlike traditional recommendation systems that simply filter students as "eligible" or "not eligible," this system:

✅ **Explains WHY** a student is or isn't eligible  
✅ **Identifies WHAT** is missing from their profile  
✅ **Guides HOW** to improve and become eligible  

### The Problem

Students in Tier-2 and Tier-3 colleges struggle to:
- Understand complex eligibility criteria
- Know what they're missing when rejected
- Find mentorship and guidance
- Navigate scattered opportunity information

### Our Solution

An AI-powered system that treats eligibility as a **journey, not a gate**—helping students understand their current standing and providing a clear roadmap for growth.

---

## 🏗️ Architecture

```
┌─────────────┐
│   Student   │ (Upload Resume / Manual Input)
└──────┬──────┘
       │
       v
┌─────────────────────────────────────┐
│         React Frontend              │
│  Profile • Search • Analysis        │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────────────────────────────┐
│       Python Flask Backend          │
│  Profile API • Search API           │
│  Reasoning API (Gemini)             │
└──────┬──────────────────────────────┘
       │
       v
┌──────────────┬──────────────┬───────────────┐
│  Gemini AI   │ Google Search│  Firebase     │
│  (Reasoning) │ (Discovery)  │  (Storage)    │
└──────────────┴──────────────┴───────────────┘
```

### Tech Stack

- **Frontend**: React + Vite
- **Backend**: Python + Flask
- **AI**: Google Gemini API
- **Search**: Google Programmable Search Engine
- **Database**: Firebase Firestore
- **Resume Parsing**: PyPDF2 + Gemini

---

## 📁 Project Structure

```
orbit/
├── backend/
│   ├── app.py                    # Flask application
│   ├── services/
│   │   ├── firebase_service.py   # Firebase operations
│   │   ├── profile_service.py    # Resume parsing, profile management
│   │   ├── opportunity_service.py # Google Search integration
│   │   └── reasoning_service.py  # Gemini AI reasoning
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProfileBuilder.jsx
│   │   │   └── OpportunityExplorer.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── docs/
├── ARCHITECTURE.md
├── GEMINI_PROMPTS.md
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key
- Google Programmable Search credentials
- Firebase project

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your credentials:
   # - GEMINI_API_KEY (required)
   # - GEMINI_API_KEY_2 (optional - for load balancing to avoid rate limits)
   # - GOOGLE_SEARCH_API_KEY
   # - GOOGLE_SEARCH_ENGINE_ID
   # - FIREBASE_CONFIG_PATH (or FIREBASE_CONFIG_JSON)
   ```
   
   **💡 Load Balancing Tip**: Add a second Gemini API key (`GEMINI_API_KEY_2`) to automatically distribute requests between two keys, preventing rate limit issues during heavy demo usage.

5. **Get API Keys**

   **Gemini API Key:**
   - Visit https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy and paste into `.env`

   **Google Search:**
   - Create Programmable Search Engine: https://programmablesearchengine.google.com/
   - Get Search Engine ID
   - Enable Custom Search API in Google Cloud Console
   - Create API credentials

   **Firebase:**
   - Create Firebase project: https://console.firebase.google.com/
   - Create Firestore database
   - Download service account JSON
   - Save as `firebase-credentials.json` or set path in `.env`

6. **Run backend**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   # Copy example env file
   cp .env.example .env.local
   
   # Edit .env.local
   # VITE_API_URL=http://localhost:5000/api
   ```

4. **Run frontend**
   ```bash
   npm run dev
   ```
   App runs on `http://localhost:3000`

---

## 🎬 Demo Narrative (For Judges)

### Opening (30 seconds)

> "Traditional platforms tell students they're 'not eligible' and stop there. 
> We believe that's where the real work should begin. Our system doesn't just 
> filter—it mentors. It explains why, identifies gaps, and provides a clear 
> roadmap to eligibility."

### Demo Flow (5 minutes)

**1. Profile Creation** (1 min)
- Show resume upload feature
- Demonstrate AI parsing with Gemini
- OR show manual profile creation
- **Judge takeaway**: "AI extracts structured data automatically"

**2. Opportunity Discovery** (1 min)
- Search for "AI hackathon"
- Show real results from Google Search
- **Judge takeaway**: "Real opportunities, not dummy data"

**3. Eligibility Analysis** (2 mins) ⭐ **CORE FEATURE**
- Click "Check Eligibility" on an opportunity
- Show the three-part analysis:
  1. **Status Badge**: Eligible/Partially/Not Yet
  2. **"Why?" Explanation**: 
     - ✅ What criteria are met
     - ❌ What's missing
  3. **"How?" Guidance**: ⭐ **DIFFERENTIATOR**
     - Specific, actionable steps
     - Time estimates
     - Resources to use

**4. Different Scenarios** (1 min)
- Show "Eligible" case (green badge, encouragement)
- Show "Partially Eligible" (yellow, with gaps + guidance)
- Show "Not Yet Eligible" (red, but with complete roadmap)

### Closing (30 seconds)

> "This system converts rejection into direction. Every 'not yet' comes with 
> a plan. For students in underserved colleges who lack mentors, this provides 
> AI-powered guidance at scale—transparent, actionable, and encouraging."

---

## 💡 Key Differentiators

| Feature | Traditional Systems | Our System |
|---------|-------------------|------------|
| **Eligibility Check** | Binary yes/no | Status + Explanation |
| **When Not Eligible** | "Sorry, not eligible" | "Here's why + how to improve" |
| **Data Source** | Static database | Live Google Search |
| **AI Usage** | Matching algorithm | Semantic reasoning + guidance |
| **Student Experience** | Discouraging | Developmental |

---

## 🧠 Prompt Engineering Highlights

Our Gemini prompts are designed with:

1. **Structured Output**: Enforces JSON schema
2. **Encouragement Bias**: Never discouraging language
3. **Specificity Rules**: Avoid vague advice
4. **Mentor Tone**: Plain English, not academic
5. **Action Orientation**: Every gap gets next steps

See [GEMINI_PROMPTS.md](GEMINI_PROMPTS.md) for full templates.

---

## 📊 Sample API Responses

### Eligibility Analysis Response

```json
{
  "reasoning_id": "uuid-here",
  "eligibility_status": "Partially Eligible",
  "reasons_met": [
    "Student is in 3rd year B.Tech Computer Science (meets education requirement)",
    "Shows strong interest in AI/ML through coursework"
  ],
  "reasons_not_met": [
    "No hands-on ML project experience mentioned",
    "Eligibility requires demonstrable ML projects"
  ],
  "missing_skills": [
    "Practical experience with ML frameworks (TensorFlow, PyTorch)"
  ],
  "missing_experience": [
    "Completed ML projects or Kaggle competitions"
  ],
  "confidence_score": 65,
  "explanation_simple": "You're close! You have the educational background, but this opportunity wants to see hands-on ML projects. The good news: you can build that experience quickly with focused effort.",
  "next_steps": [
    {
      "action": "Complete a beginner ML project (e.g., classification model on Kaggle dataset)",
      "reason": "Demonstrates practical skills that match the opportunity's requirements",
      "time_estimate": "2-3 weeks"
    },
    {
      "action": "Document your project on GitHub with clear README",
      "reason": "Makes your work visible and showcases your abilities",
      "time_estimate": "2-3 days"
    }
  ]
}
```

---

## 🎯 Success Metrics (For Demo)

During demo, highlight:

1. **Speed**: Profile → Search → Analysis in under 60 seconds
2. **Real Data**: Live Google Search results
3. **Explainability**: Every decision has reasoning
4. **Guidance**: No "not eligible" without roadmap
5. **Judge Comprehension**: System understandable in 30 seconds

---

## 🚀 Future Enhancements (Post-Hackathon)

- [ ] WhatsApp integration for wider reach
- [ ] Progress tracking dashboard
- [ ] Resource recommendations (courses, projects)
- [ ] Community features (mentorship matching)
- [ ] Multi-language support
- [ ] Mobile app

---

## 🛠️ Troubleshooting

### Backend issues

**Module not found:**
```bash
pip install -r requirements.txt
```

**Firebase connection error:**
- Check `FIREBASE_CONFIG_PATH` in `.env`
- Verify service account JSON is valid
- Ensure Firestore is enabled in Firebase console

**Gemini API error:**
- Verify API key in `.env`
- Check API quota: https://makersuite.google.com/
- Ensure billing is enabled if needed

### Frontend issues

**Port already in use:**
```bash
# Change port in vite.config.js
server: { port: 3001 }
```

**API connection error:**
- Ensure backend is running on port 5000
- Check `VITE_API_URL` in `.env.local`
- Verify CORS is enabled in Flask

---

## 📝 API Endpoints

### Profile
- `POST /api/profile/parse_resume` - Upload & parse resume
- `POST /api/profile/create` - Create profile manually
- `GET /api/profile/{id}` - Get profile

### Opportunities
- `POST /api/opportunities/search` - Search opportunities
- `GET /api/opportunities/cached` - Get cached results
- `GET /api/opportunities/{id}` - Get specific opportunity

### Reasoning (Core Intelligence)
- `POST /api/reasoning/analyze` - Analyze eligibility
- `POST /api/reasoning/batch` - Batch analyze multiple
- `GET /api/reasoning/results/{id}` - Get cached analysis

### Utility
- `GET /api/health` - Health check
- `GET /api/info` - API information

---

## 👥 Team & Credits

Built for 24-hour hackathon demonstrating:
- AI reasoning with Gemini
- Real-time data with Google Search
- Firebase integration
- React best practices

**Core Philosophy**: Eligibility is a journey, not a gate.

---

## 📄 License

MIT License - Built for educational and demonstration purposes.

---

## 🤝 Contributing

This is a hackathon MVP. For production use:
1. Add authentication
2. Implement rate limiting
3. Add comprehensive error handling
4. Improve caching strategies
5. Add analytics
6. Enhance security

---

## 📞 Support

For demo questions or technical issues:
- Review [ARCHITECTURE.md](ARCHITECTURE.md)
- Check [GEMINI_PROMPTS.md](GEMINI_PROMPTS.md)
- Verify environment variables

---

**Remember**: This system doesn't decide who deserves opportunities—it helps students understand how to prepare for them.

🎯 **Every "Not Yet Eligible" is a roadmap to "Ready"**
