# API Documentation

## Base URL

```
http://localhost:5000/api
```

---

## Authentication

Currently **no authentication** required (demo mode). For production, implement JWT or OAuth.

---

## Endpoints

### Health & Info

#### `GET /api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Opportunity Intelligence API",
  "version": "1.0.0"
}
```

#### `GET /api/info`

Get API information and available endpoints.

**Response:**
```json
{
  "name": "AI-Powered Opportunity Intelligence System",
  "description": "Never just say 'Not Eligible' — Always explain why and guide how to improve",
  "endpoints": {
    "profiles": [...],
    "opportunities": [...],
    "reasoning": [...]
  }
}
```

---

## Profile Management

### `POST /api/profile/parse_resume`

Parse a resume PDF and create a structured profile.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `resume` field containing PDF file

**Example (curl):**
```bash
curl -X POST http://localhost:5000/api/profile/parse_resume \
  -F "resume=@/path/to/resume.pdf"
```

**Response:**
```json
{
  "profile_id": "uuid-here",
  "profile_data": {
    "education": {
      "degree": "B.Tech",
      "major": "Computer Science",
      "institution": "ABC Institute",
      "year": "3rd year",
      "cgpa_or_percentage": "8.5"
    },
    "skills": {
      "programming_languages": ["Python", "Java"],
      "frameworks": ["React", "Django"],
      "tools": ["Git", "Docker"],
      "domains": ["Machine Learning", "Web Development"]
    },
    "experience": [...],
    "achievements": [...],
    "interests": [...],
    "self_description": "..."
  }
}
```

**Status Codes:**
- `201 Created`: Profile created successfully
- `400 Bad Request`: No file provided or invalid file
- `500 Internal Server Error`: Parsing failed

---

### `POST /api/profile/create`

Create a profile from manual input.

**Request:**
```json
{
  "education": {
    "degree": "B.Tech",
    "major": "Computer Science",
    "institution": "XYZ College",
    "year": "2nd year",
    "cgpa_or_percentage": "7.8"
  },
  "skills": {
    "programming_languages": ["Python", "JavaScript"],
    "frameworks": ["React", "Flask"],
    "tools": ["Git"],
    "domains": ["Web Development"]
  },
  "experience": [
    {
      "type": "project",
      "title": "E-commerce Website",
      "organization": "Personal",
      "duration": "2 months",
      "description": "Built using React and Node.js"
    }
  ],
  "achievements": ["Best Project Award 2025"],
  "interests": ["AI", "Web Development"],
  "self_description": "Passionate developer interested in AI"
}
```

**Response:**
```json
{
  "profile_id": "uuid-here",
  "profile_data": { ... }
}
```

**Status Codes:**
- `201 Created`: Profile created
- `400 Bad Request`: Invalid profile structure
- `500 Internal Server Error`: Failed to save

---

### `GET /api/profile/{profile_id}`

Get a profile by ID.

**Response:**
```json
{
  "profile_id": "uuid-here",
  "profile": { ... },
  "resume_text": "...",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Status Codes:**
- `200 OK`: Profile found
- `404 Not Found`: Profile doesn't exist

---

## Opportunity Discovery

### `POST /api/opportunities/search`

Search for opportunities using Google Programmable Search.

**Request:**
```json
{
  "query": "AI hackathon India 2026",
  "opportunity_type": "hackathon"
}
```

Parameters:
- `query` (required): Search query string
- `opportunity_type` (optional): Filter by type (hackathon, internship, fellowship)

**Response:**
```json
{
  "opportunities": [
    {
      "opportunity_id": "uuid-here",
      "title": "Smart India Hackathon 2026",
      "organizer": "Government of India",
      "link": "https://sih.gov.in",
      "snippet": "Open to undergraduate and postgraduate students...",
      "eligibility_text": "Students must be enrolled in recognized institutions...",
      "deadline": "January 31, 2026",
      "type": "hackathon",
      "source": "google_search",
      "cached_at": "timestamp"
    },
    ...
  ],
  "count": 10,
  "query": "hackathon AI hackathon India 2026 students",
  "cached": true
}
```

**Status Codes:**
- `200 OK`: Search successful
- `400 Bad Request`: Query missing
- `500 Internal Server Error`: Search failed

---

### `GET /api/opportunities/cached`

Get recently cached opportunities.

**Query Parameters:**
- `limit` (optional): Number of results (default: 20)
- `type` (optional): Filter by opportunity type

**Example:**
```
GET /api/opportunities/cached?limit=10&type=internship
```

**Response:**
```json
{
  "opportunities": [...],
  "count": 10
}
```

---

### `GET /api/opportunities/{opportunity_id}`

Get a specific opportunity by ID.

**Response:**
```json
{
  "opportunity_id": "uuid-here",
  "title": "...",
  "organizer": "...",
  "link": "...",
  "snippet": "...",
  "eligibility_text": "...",
  "deadline": "...",
  "type": "...",
  "cached_at": "..."
}
```

**Status Codes:**
- `200 OK`: Opportunity found
- `404 Not Found`: Opportunity doesn't exist

---

## Eligibility Reasoning (Core Intelligence)

### `POST /api/reasoning/analyze`

Analyze student eligibility for an opportunity using Gemini AI.

**Request:**
```json
{
  "profile_id": "student-uuid",
  "opportunity_id": "opportunity-uuid"
}
```

**Response:**
```json
{
  "reasoning_id": "uuid-here",
  "eligibility_status": "Partially Eligible",
  "reasons_met": [
    "Student is in 3rd year B.Tech CS (meets education requirement)",
    "Has Python programming skills"
  ],
  "reasons_not_met": [
    "No ML project experience mentioned",
    "Lacks hands-on ML framework experience"
  ],
  "missing_skills": [
    "TensorFlow or PyTorch experience",
    "Model training and evaluation"
  ],
  "missing_experience": [
    "Completed ML projects",
    "Kaggle competitions"
  ],
  "confidence_score": 65,
  "explanation_simple": "You have the foundation, but need hands-on ML projects. This gap is achievable in 2-3 weeks with focused effort.",
  "next_steps": [
    {
      "action": "Complete a beginner ML project (e.g., image classifier)",
      "reason": "Demonstrates practical skills matching requirements",
      "time_estimate": "2-3 weeks"
    },
    {
      "action": "Create GitHub repository with documentation",
      "reason": "Makes your work visible to recruiters",
      "time_estimate": "2-3 days"
    },
    {
      "action": "Take TensorFlow course on Coursera",
      "reason": "Fills specific framework knowledge gap",
      "time_estimate": "2-3 weeks"
    }
  ],
  "cached": false
}
```

**Note:** If analysis already exists, returns cached result with `"cached": true`.

**Status Codes:**
- `200 OK`: Analysis complete or cached
- `400 Bad Request`: Missing profile_id or opportunity_id
- `500 Internal Server Error`: Analysis failed

---

### `POST /api/reasoning/batch`

Analyze eligibility for multiple opportunities at once.

**Request:**
```json
{
  "profile_id": "student-uuid",
  "opportunity_ids": [
    "opportunity-uuid-1",
    "opportunity-uuid-2",
    "opportunity-uuid-3"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "opportunity_id": "opportunity-uuid-1",
      "analysis": { ... },
      "cached": false
    },
    {
      "opportunity_id": "opportunity-uuid-2",
      "analysis": { ... },
      "cached": true
    },
    {
      "opportunity_id": "opportunity-uuid-3",
      "error": "Opportunity not found"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Batch analysis complete
- `400 Bad Request`: Missing required fields

---

### `GET /api/reasoning/results/{reasoning_id}`

Get a cached reasoning result by ID.

**Response:**
```json
{
  "reasoning_id": "uuid-here",
  "profile_id": "...",
  "opportunity_id": "...",
  "analysis": { ... },
  "analyzed_at": "timestamp"
}
```

**Status Codes:**
- `200 OK`: Result found
- `404 Not Found`: Result doesn't exist

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

**Common Status Codes:**
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

Currently **no rate limiting** (demo). For production:
- Implement per-user rate limits
- Cache Gemini API responses
- Batch requests when possible

---

## Data Models

### Profile Structure

```typescript
{
  education: {
    degree: string,
    major: string,
    institution: string,
    year: string,
    cgpa_or_percentage: string
  },
  skills: {
    programming_languages: string[],
    frameworks: string[],
    tools: string[],
    domains: string[]
  },
  experience: Array<{
    type: "internship" | "project" | "job" | "volunteer",
    title: string,
    organization: string,
    duration: string,
    description: string
  }>,
  achievements: string[],
  interests: string[],
  self_description: string
}
```

### Opportunity Structure

```typescript
{
  opportunity_id: string,
  title: string,
  organizer: string,
  link: string,
  snippet: string,
  eligibility_text: string,
  deadline: string | null,
  type: "hackathon" | "internship" | "fellowship" | "scholarship" | "competition" | "program",
  source: "google_search",
  cached_at: timestamp
}
```

### Analysis Structure

```typescript
{
  reasoning_id: string,
  eligibility_status: "Eligible" | "Partially Eligible" | "Not Yet Eligible",
  reasons_met: string[],
  reasons_not_met: string[],
  missing_skills: string[],
  missing_experience: string[],
  confidence_score: number (0-100),
  explanation_simple: string,
  next_steps: Array<{
    action: string,
    reason: string,
    time_estimate: string
  }>
}
```

---

## Testing

### Using curl

```bash
# Health check
curl http://localhost:5000/api/health

# Create profile
curl -X POST http://localhost:5000/api/profile/create \
  -H "Content-Type: application/json" \
  -d @profile.json

# Search opportunities
curl -X POST http://localhost:5000/api/opportunities/search \
  -H "Content-Type: application/json" \
  -d '{"query": "AI hackathon", "opportunity_type": "hackathon"}'

# Analyze eligibility
curl -X POST http://localhost:5000/api/reasoning/analyze \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "uuid-1", "opportunity_id": "uuid-2"}'
```

### Using Python requests

```python
import requests

API_BASE = "http://localhost:5000/api"

# Create profile
profile_data = {...}
response = requests.post(f"{API_BASE}/profile/create", json=profile_data)
profile = response.json()

# Search opportunities
response = requests.post(f"{API_BASE}/opportunities/search", json={
    "query": "AI hackathon",
    "opportunity_type": "hackathon"
})
opportunities = response.json()["opportunities"]

# Analyze eligibility
response = requests.post(f"{API_BASE}/reasoning/analyze", json={
    "profile_id": profile["profile_id"],
    "opportunity_id": opportunities[0]["opportunity_id"]
})
analysis = response.json()
```

---

## Performance Notes

- **Profile parsing**: 2-5 seconds (Gemini AI)
- **Opportunity search**: 1-3 seconds (Google API + caching)
- **Eligibility analysis**: 3-8 seconds (Gemini AI)

**Optimization strategies**:
- Results are cached in Firebase
- Duplicate analyses return cached data
- Batch operations supported

---

## CORS Configuration

CORS is enabled for all origins in development mode. For production:

```python
# app.py
CORS(app, origins=["https://yourdomain.com"])
```

---

## Webhooks (Future)

For production, consider adding webhooks for:
- Profile creation events
- New opportunity matches
- Analysis completion notifications
