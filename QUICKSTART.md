# 🚀 Quick Start Guide

## 30-Second Setup

### 1. Install Dependencies

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Frontend (new terminal)
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Backend
cd backend
cp .env.example .env

# Edit .env and add MINIMUM required:
# GEMINI_API_KEY=your_key_here
# (Firebase and Google Search can use mock data for testing)

# Frontend
cd frontend
cp .env.example .env.local
# Default values work for local development
```

### 3. Get Gemini API Key (2 minutes)

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy key
4. Paste into `backend/.env`

### 4. Run Application

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Open Browser

Navigate to: `http://localhost:3000`

---

## Testing Without Full Setup

The application includes **mock data** fallbacks:

- **Without Google Search API**: Returns sample opportunities
- **Without Firebase**: Stores data in memory (non-persistent)
- **Requires Gemini**: AI reasoning needs valid API key

So you can test with ONLY a Gemini API key!

---

## Sample Test Flow

1. **Create Profile**
   - Click "Enter Manually"
   - Fill in:
     - Degree: B.Tech
     - Major: Computer Science
     - Year: 3rd year
     - Skills: Python, React, Machine Learning
     - Interests: AI, Web Development

2. **Search Opportunities**
   - Type: "AI hackathon"
   - Click Search
   - See mock results if no API key

3. **Check Eligibility**
   - Click "Check Eligibility" on any opportunity
   - See AI analysis

---

## Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Backend - change in app.py: port=5001
# Frontend - change in vite.config.js: port: 3001
```

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in `backend/` directory
- Verify key format: `GEMINI_API_KEY=AIza...`
- No quotes around the key

### "CORS error"
- Ensure backend is running on port 5000
- Check `vite.config.js` proxy settings

---

## Production Setup

For full production deployment:

1. **Get all API keys**:
   - Gemini API
   - Google Search API + Engine ID
   - Firebase service account

2. **Configure Firebase**:
   - Create Firestore database
   - Download service account JSON
   - Set path in `.env`

3. **Deploy**:
   - Backend: Heroku, GCP, AWS
   - Frontend: Vercel, Netlify, Firebase Hosting

---

## API Key Quick Links

| Service | Get Key | Documentation |
|---------|---------|---------------|
| Gemini | [Get Key](https://makersuite.google.com/app/apikey) | [Docs](https://ai.google.dev/docs) |
| Google Search | [Console](https://console.cloud.google.com/) | [Setup Guide](https://developers.google.com/custom-search/v1/overview) |
| Firebase | [Console](https://console.firebase.google.com/) | [Setup](https://firebase.google.com/docs/firestore/quickstart) |

---

## Need Help?

1. Check `README.md` for detailed setup
2. Review `ARCHITECTURE.md` for system design
3. See `DEMO_SCRIPT.md` for usage examples

---

**Fastest path to demo**: Get Gemini API key → Run → Test with mock data
