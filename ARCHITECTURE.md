# System Architecture: AI-Powered Opportunity Intelligence System

## Core Philosophy
**"Never just say 'Not Eligible' — Always explain why and guide how to improve"**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         STUDENT                                  │
│                    (Resume / Manual Input)                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND                                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Profile     │  │  Opportunity │  │  Eligibility        │  │
│  │  Builder     │  │  Explorer    │  │  Explainer          │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│                    PYTHON BACKEND (Flask)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Profile API │  │  Search API  │  │  Reasoning API      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────────────┘  │
│         │                  │                  │                  │
│         v                  v                  v                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Resume      │  │  Google      │  │  Gemini AI          │  │
│  │  Parser      │  │  Search      │  │  Reasoning          │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│                    FIREBASE FIRESTORE                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Student     │  │  Opportunity │  │  Reasoning          │  │
│  │  Profiles    │  │  Cache       │  │  Results            │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. **Frontend (React)**

#### Components:
- **ProfileBuilder**
  - Resume upload (PDF)
  - Manual form input
  - Preview structured profile
  
- **OpportunityExplorer**
  - Search opportunities by keywords
  - Display real-time results
  - Filter by type (hackathon, internship, fellowship)
  
- **EligibilityExplainer**
  - Color-coded badges (Green/Yellow/Red)
  - Expandable "Why?" section
  - Expandable "How to improve" section
  - Non-discouraging tone

#### Key Features:
- Single page application
- No authentication required (demo mode)
- Judge-friendly (30-second comprehension)

---

### 2. **Backend (Python Flask)**

#### API Endpoints:

```python
POST   /api/profile/parse_resume     # Upload & parse resume
POST   /api/profile/create           # Create profile manually
GET    /api/profile/{id}             # Get profile

POST   /api/opportunities/search     # Search using Google API
GET    /api/opportunities/cached     # Get cached results

POST   /api/reasoning/analyze        # Analyze eligibility
GET    /api/reasoning/results/{id}   # Get cached results
```

#### Services:

**ResumeParser**
- Extract text from PDF
- Identify sections (education, skills, experience)
- Structure into JSON

**OpportunitySearchService**
- Query Google Programmable Search Engine
- Extract: title, link, organizer, eligibility text
- Cache in Firebase

**EligibilityReasoningService**
- Use Gemini API for semantic reasoning
- Generate structured eligibility analysis
- Create actionable guidance

---

### 3. **AI Layer (Gemini API)**

#### Prompt Design:

**Eligibility Analysis Prompt:**
```
You are an expert career advisor analyzing student eligibility for opportunities.

STUDENT PROFILE:
{profile_json}

OPPORTUNITY CRITERIA:
{eligibility_text}

TASK: Determine eligibility and provide guidance.

OUTPUT (JSON):
{
  "eligibility_status": "Eligible | Partially Eligible | Not Yet Eligible",
  "reasons_met": ["list of met criteria"],
  "reasons_not_met": ["list of unmet criteria"],
  "missing_skills": ["specific skills to acquire"],
  "missing_experience": ["experience gaps"],
  "confidence_score": 85,
  "explanation_simple": "Plain English summary",
  "next_steps": [
    {
      "action": "Specific action",
      "reason": "Why it matters",
      "time_estimate": "Realistic timeframe"
    }
  ]
}

RULES:
- NEVER just say "not eligible" without explanation
- Be encouraging, not discouraging
- Provide actionable steps
- Be specific about gaps
- Focus on growth, not rejection
```

---

### 4. **Search Layer (Google Programmable Search)**

#### Search Strategy:
- Query templates: "student hackathon India 2026"
- Query templates: "internship undergraduate technology"
- Query templates: "fellowship program engineering students"

#### Data Extraction:
- Title, URL, snippet
- Parse snippet for dates, eligibility hints
- Store raw text for Gemini analysis

---

### 5. **Database (Firebase Firestore)**

#### Collections:

**students**
```json
{
  "id": "uuid",
  "profile": {
    "education": {...},
    "skills": [...],
    "experience": [...],
    "interests": [...],
    "self_description": "..."
  },
  "resume_text": "...",
  "created_at": "timestamp"
}
```

**opportunities**
```json
{
  "id": "uuid",
  "title": "...",
  "organizer": "...",
  "link": "...",
  "eligibility_text": "...",
  "deadline": "...",
  "type": "hackathon|internship|fellowship",
  "cached_at": "timestamp"
}
```

**reasoning_results**
```json
{
  "id": "uuid",
  "student_id": "...",
  "opportunity_id": "...",
  "analysis": {...},
  "analyzed_at": "timestamp"
}
```

---

## Data Flow

### User Journey: Profile Creation
1. Student uploads resume OR fills form
2. Backend parses resume → structured JSON
3. Store in Firebase `students` collection
4. Return profile ID to frontend

### User Journey: Opportunity Discovery
1. Student enters keywords (e.g., "AI hackathon")
2. Backend queries Google Programmable Search
3. Extract title, link, eligibility text
4. Cache in Firebase `opportunities`
5. Return list to frontend

### User Journey: Eligibility Analysis
1. Student clicks "Check Eligibility" on opportunity
2. Backend fetches: student profile + opportunity
3. Send both to Gemini API with reasoning prompt
4. Gemini returns structured analysis
5. Cache in Firebase `reasoning_results`
6. Frontend displays:
   - Badge (color-coded)
   - "Why?" explanation
   - "How to improve?" steps

---

## Technology Integration

### Google Technologies (MANDATORY)

| Technology | Purpose | Integration Point |
|------------|---------|-------------------|
| **Gemini API** | Eligibility reasoning, guidance generation | `EligibilityReasoningService` |
| **Google Programmable Search** | Discover real opportunities | `OpportunitySearchService` |
| **Firebase Firestore** | Store profiles, opportunities, results | All services |

---

## Hackathon-Specific Optimizations

### What Makes This Demo-Ready:
1. **Real Data**: Uses live Google Search, not dummy datasets
2. **Explainability**: Every decision has a reason
3. **Guidance**: Converts "no" into "not yet, here's how"
4. **Judge Friendly**: Simple UI, clear narrative

### What We're NOT Building:
- Authentication system
- Payment integration
- Mobile app
- Complex dashboards
- Admin panel

---

## Success Metrics (Demo)

During the demo, we'll show:
1. **Profile Creation**: 30 seconds
2. **Opportunity Search**: Real results in 5 seconds
3. **Eligibility Analysis**: Clear explanation in 10 seconds
4. **Guidance Generation**: Actionable steps displayed

**Judge Takeaway**: "This doesn't just filter students—it guides them."

---

## Technical Implementation Notes

### Environment Variables Required:
```
GEMINI_API_KEY=your_key
GOOGLE_SEARCH_ENGINE_ID=your_id
GOOGLE_SEARCH_API_KEY=your_key
FIREBASE_CONFIG=your_config_json
```

### Dependencies:
- Python: Flask, google-generativeai, firebase-admin, PyPDF2
- React: axios, react-router-dom, tailwindcss

### Estimated Build Time:
- Backend: 6-8 hours
- Frontend: 4-6 hours
- Integration: 2-3 hours
- Testing: 2-3 hours
**Total: 14-20 hours** (fits 24-hour hackathon)

---

## Differentiator for Judges

**Most systems**: Binary filter (eligible/not)
**This system**: Reasoning engine (why + how)

**Most systems**: Gate-keeping
**This system**: Mentorship at scale

**Most systems**: Black box
**This system**: Transparent guidance

---

## Next Steps (Implementation Order)

1. ✅ Architecture design
2. ⏳ Prompt templates
3. ⏳ Backend APIs
4. ⏳ Frontend components
5. ⏳ Integration testing
6. ⏳ Demo preparation
