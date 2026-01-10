# 🚀 ORBIT Deployment Guide

## Architecture
- **Frontend**: React + Vite → Deploy to **Vercel** (recommended)
- **Backend**: Flask + Python → Deploy to **Render** (recommended)
- **Database**: Firebase Firestore (already cloud-hosted)

---

## 📋 Prerequisites

Before deploying, ensure you have:
1. ✅ GitHub account
2. ✅ Vercel account (sign up at vercel.com)
3. ✅ Render account (sign up at render.com)
4. ✅ Firebase credentials JSON file
5. ✅ Gemini API keys (2 recommended for load balancing)
6. ✅ Google Custom Search API key and Engine ID

---

## 🔧 Step 1: Push to GitHub

```bash
# Initialize git if not already done
cd C:\Users\JAYAN\Downloads\orbit
git init
git add .
git commit -m "Initial commit - ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/orbit.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy Backend to Render

### 2.1 Create New Web Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `orbit` repository

### 2.2 Configure Build Settings
```
Name: orbit-backend
Region: Choose nearest to you
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 2.3 Set Environment Variables
In Render dashboard, add these environment variables:

```
FLASK_ENV=production
GEMINI_API_KEY=your_gemini_api_key_1
GEMINI_API_KEY_2=your_gemini_api_key_2
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

### 2.4 Add Firebase Credentials
**Important**: Don't commit `firebase-credentials.json` to GitHub!

Option A: Use Render Secret Files
1. In Render dashboard → your service → "Environment"
2. Click "Secret Files"
3. Add new file:
   - **Filename**: `firebase-credentials.json`
   - **Content**: Paste your Firebase JSON content

Option B: Use Environment Variable
1. Convert Firebase JSON to single line
2. Add as environment variable: `FIREBASE_CREDENTIALS_JSON`

### 2.5 Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Note your backend URL: `https://orbit-backend-XXXX.onrender.com`

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### 3.2 Deploy via Vercel Dashboard (Recommended)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

### 3.3 Set Environment Variables
In Vercel project settings → "Environment Variables":

```
VITE_API_URL=https://orbit-backend-XXXX.onrender.com/api
```

⚠️ **Important**: Replace `orbit-backend-XXXX.onrender.com` with your actual Render URL

### 3.4 Deploy
- Click **"Deploy"**
- Wait 2-3 minutes
- Your app will be live at: `https://orbit-XXXX.vercel.app`

---

## 🔐 Step 4: Update CORS Settings

After deployment, update backend CORS to allow your frontend domain:

1. In your code, update `backend/app.py`:
```python
CORS(app, origins=[
    "https://orbit-XXXX.vercel.app",  # Your Vercel URL
    "http://localhost:5173",           # Keep for local development
    "http://localhost:3000"
])
```

2. Or set as environment variable in Render:
```
ALLOWED_ORIGINS=https://orbit-XXXX.vercel.app,http://localhost:5173
```

3. Commit and push changes - Render will auto-redeploy

---

## ✅ Step 5: Test Deployment

1. Visit your Vercel URL: `https://orbit-XXXX.vercel.app`
2. Test authentication (register/login)
3. Upload resume
4. Search for opportunities
5. Check eligibility analysis

---

## 🔍 Troubleshooting

### Backend Issues

**Problem**: 500 Internal Server Error
- Check Render logs: Dashboard → Your Service → "Logs"
- Verify all environment variables are set
- Ensure Firebase credentials are properly uploaded

**Problem**: Firebase connection failed
- Verify `firebase-credentials.json` is uploaded as Secret File
- Check Firebase project settings
- Ensure service account has Firestore permissions

**Problem**: Gemini API errors
- Verify API keys are valid
- Check API quota limits
- Ensure billing is enabled in Google Cloud

### Frontend Issues

**Problem**: Can't connect to backend
- Verify `VITE_API_URL` environment variable
- Check backend is running (visit backend URL directly)
- Check browser console for CORS errors

**Problem**: Environment variables not working
- In Vercel, environment variables must start with `VITE_`
- Redeploy after adding/changing environment variables

### Common Issues

**Problem**: Resume parsing timeout
- Render free tier may have cold starts (first request is slow)
- Upgrade to paid tier for better performance
- Or use Railway/Heroku alternatives

**Problem**: Search results not loading
- Verify Google Custom Search API key
- Check API quota hasn't exceeded
- Ensure Search Engine ID is correct

---

## 📊 Monitoring

### Render (Backend)
- View logs: Dashboard → Service → "Logs"
- Monitor metrics: Dashboard → Service → "Metrics"
- Set up alerts: Dashboard → Service → "Alerts"

### Vercel (Frontend)
- View deployment logs: Project → "Deployments" → Click deployment
- Monitor analytics: Project → "Analytics"
- Check performance: Project → "Speed Insights"

---

## 💰 Pricing

### Free Tier Limits

**Render**:
- ✅ 750 hours/month free
- ⚠️ Spins down after 15 mins of inactivity (cold starts)
- ✅ Automatic SSL
- ✅ Custom domains

**Vercel**:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic SSL
- ✅ Custom domains

### Upgrade Recommendations
- Render: $7/month for 400+ build hours, no cold starts
- Vercel: $20/month for team features, more bandwidth

---

## 🚀 Alternative Deployment Options

### Backend Alternatives
1. **Railway** (railway.app) - Similar to Render, $5/month
2. **Heroku** ($7/month) - More established, but pricier
3. **Google Cloud Run** - Pay per use, scales to zero
4. **Azure App Service** - Good for enterprise
5. **AWS Elastic Beanstalk** - More complex setup

### Frontend Alternatives
1. **Netlify** - Similar to Vercel
2. **GitHub Pages** - Free but static only (needs SPA routing fix)
3. **Cloudflare Pages** - Fast CDN, generous free tier
4. **Firebase Hosting** - Since you're already using Firebase

---

## 🔄 Continuous Deployment

Both Render and Vercel support automatic deployments:

1. **Push to GitHub** → Automatic deployment
2. **Pull Request** → Preview deployment (Vercel)
3. **Merge to main** → Production deployment

No manual redeployment needed! 🎉

---

## 📝 Post-Deployment Checklist

- [ ] Backend URL is live and accessible
- [ ] Frontend URL is live and shows landing page
- [ ] User registration works
- [ ] User login works
- [ ] Resume upload and parsing works
- [ ] Personalized suggestions load
- [ ] Search functionality works
- [ ] Eligibility analysis works
- [ ] Custom domain configured (optional)
- [ ] Analytics set up (optional)

---

## 🎓 Getting API Keys

### Gemini API Keys
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key
4. Repeat for second key (load balancing)

### Google Custom Search API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Custom Search API"
3. Create credentials → API Key
4. Create Custom Search Engine at [CSE Panel](https://programmablesearchengine.google.com/)
5. Get your Search Engine ID

### Firebase Setup
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Project Settings → Service Accounts
4. Generate new private key
5. Download JSON file

---

## 🎉 You're All Set!

Your ORBIT application is now live and accessible worldwide!

**Share your deployment URLs**:
- Frontend: `https://orbit-XXXX.vercel.app`
- Backend: `https://orbit-backend-XXXX.onrender.com`

Need help? Check the logs or reach out to the community!
