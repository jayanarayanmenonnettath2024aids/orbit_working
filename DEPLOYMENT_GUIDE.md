# 🚀 ORBIT Deployment Guide

Complete step-by-step guide to deploy ORBIT (Opportunity Intelligence System) to production.

---

## 📋 Prerequisites

Before starting deployment, ensure you have:

- ✅ GitHub account with `orbit_working` repository access
- ✅ Vercel account (for frontend)
- ✅ Render account (for backend)
- ✅ Google Gemini API keys (2 recommended for load balancing)
- ✅ Google Programmable Search Engine ID
- ✅ Firebase project with Firestore enabled
- ✅ Firebase Admin SDK credentials JSON file

---

## 🗂️ Project Structure

```
orbit/
├── frontend/           # React + Vite frontend
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json
│   └── .env.example
│
└── backend/            # Flask API backend
    ├── services/
    ├── app.py
    ├── requirements.txt
    ├── Procfile
    └── .env.example
```

---

## 📦 Step 1: Verify Deployment Files

### Backend Files Check

#### ✅ `backend/requirements.txt`
```txt
Flask==3.0.0
flask-cors==4.0.0
gunicorn==21.2.0
google-generativeai==0.3.2
google-api-python-client==2.110.0
firebase-admin==6.4.0
PyPDF2==3.0.1
python-dotenv==1.0.0
requests==2.31.0
python-dateutil==2.8.2
```

#### ✅ `backend/Procfile`
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

#### ✅ `backend/.env.example`
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY_2=your_gemini_api_key_here_2
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

### Frontend Files Check

#### ✅ `frontend/package.json` (key dependencies)
```json
{
  "dependencies": {
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "recharts": "^3.6.0"
  },
  "scripts": {
    "build": "vite build",
    "dev": "vite"
  }
}
```

#### ✅ `frontend/vercel.json`
```json
{
  "buildCommand": "npm install && npm run build",
  "framework": "vite",
  "outputDirectory": "dist"
}
```

---

## 🔧 Step 2: Backend Deployment to Render

### 2.1 Create Render Web Service

1. **Sign in to Render**: Go to [render.com](https://render.com) and log in
2. **Create New Web Service**: 
   - Click **"New +"** → **"Web Service"**
3. **Connect Repository**:
   - Select **"Connect GitHub"**
   - Choose `orbit_working` repository
   - Click **"Connect"**

### 2.2 Configure Service Settings

| Setting | Value |
|---------|-------|
| **Name** | `orbit-backend` |
| **Root Directory** | `backend` |
| **Environment** | `Python 3` |
| **Region** | Choose nearest region |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### 2.3 Configure Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `GEMINI_API_KEY` | `your_api_key_1` | Get from [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `GEMINI_API_KEY_2` | `your_api_key_2` | Optional: For load balancing |
| `GOOGLE_SEARCH_API_KEY` | `your_search_api_key` | From Google Cloud Console |
| `GOOGLE_SEARCH_ENGINE_ID` | `your_search_engine_id` | From [Programmable Search](https://programmablesearchengine.google.com/) |
| `PORT` | `10000` | Auto-set by Render |
| `FLASK_ENV` | `production` | Set to production |
| `PYTHON_VERSION` | `3.11.0` | Specify Python version |

### 2.4 Add Firebase Credentials

**Option A: Using Secret Files (Recommended)**

1. In Render dashboard, go to **"Environment"** tab
2. Scroll to **"Secret Files"** section
3. Click **"Add Secret File"**
4. Configure:
   - **Filename**: `firebase-credentials.json`
   - **Contents**: Paste your Firebase Admin SDK JSON content
   - Click **"Save"**

**Option B: Using Environment Variable**

Add environment variable:
```
FIREBASE_CREDENTIALS_JSON=<paste entire JSON as string>
```

Then update `backend/services/firebase_service.py` to read from environment variable if needed.

### 2.5 Deploy Backend

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll get a URL like: `https://orbit-backend.onrender.com`
4. **Test the backend**: Visit `https://orbit-backend.onrender.com/api/health`
   - Expected response: `{"status": "healthy", "service": "Opportunity Intelligence API"}`

---

## 🎨 Step 3: Frontend Deployment to Vercel

### 3.1 Import Project to Vercel

1. **Sign in to Vercel**: Go to [vercel.com](https://vercel.com) and log in
2. **Create New Project**:
   - Click **"Add New..."** → **"Project"**
3. **Import Repository**:
   - Click **"Import Git Repository"**
   - Select `orbit_working` repository
   - Click **"Import"**

### 3.2 Configure Project Settings

| Setting | Value |
|---------|-------|
| **Project Name** | `orbit-frontend` |
| **Framework Preset** | `Vite` (auto-detected) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (auto-detected) |
| **Output Directory** | `dist` (auto-detected) |
| **Install Command** | `npm install` (auto-detected) |

### 3.3 Configure Environment Variables

Click **"Environment Variables"** and add:

| Key | Value | Environment |
|-----|-------|-------------|
| `VITE_API_URL` | `https://orbit-backend.onrender.com/api` | Production |

**Important**: Replace `https://orbit-backend.onrender.com` with your actual Render backend URL from Step 2.5.

### 3.4 Deploy Frontend

1. Click **"Deploy"**
2. Wait for deployment (2-5 minutes)
3. Once deployed, you'll get a URL like: `https://orbit-frontend.vercel.app`
4. **Visit your live app**: Open the Vercel URL in browser

---

## 🔐 Step 4: Post-Deployment Security

### 4.1 Update CORS Configuration (Backend)

Edit `backend/app.py` CORS configuration for production:

```python
# Replace this:
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=False)

# With this:
CORS(app, 
     resources={r"/api/*": {
         "origins": [
             "https://orbit-frontend.vercel.app",  # Your Vercel domain
             "https://your-custom-domain.com"      # If you have custom domain
         ]
     }},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=False)
```

Commit and push changes to trigger redeployment.

### 4.2 Firebase Security Rules

Update Firestore security rules in Firebase Console:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null;
    }
    
    // Profiles collection
    match /profiles/{profileId} {
      allow read, write: if request.auth != null;
    }
    
    // Applications collection
    match /applications/{applicationId} {
      allow read, write: if request.auth != null;
    }
    
    // Gamification collection
    match /gamification/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // Analytics (read-only for authenticated users)
    match /analytics/{document=**} {
      allow read: if request.auth != null;
    }
  }
}
```

---

## 🧪 Step 5: Testing Deployment

### 5.1 Test Backend API

```bash
# Health check
curl https://orbit-backend.onrender.com/api/health

# API info
curl https://orbit-backend.onrender.com/api/info
```

Expected responses:
```json
// Health check
{
  "status": "healthy",
  "service": "Opportunity Intelligence API",
  "version": "1.0.0"
}

// API info
{
  "name": "AI-Powered Opportunity Intelligence System",
  "description": "Never just say 'Not Eligible' — Always explain why and guide how to improve"
}
```

### 5.2 Test Frontend

1. Open `https://orbit-frontend.vercel.app` in browser
2. **Test Registration**:
   - Click "Sign Up"
   - Create new account
   - Verify email/password validation
3. **Test Login**:
   - Login with created account
   - Verify redirect to dashboard
4. **Test Features**:
   - ✅ Dashboard loads
   - ✅ Opportunity search works
   - ✅ Profile creation works
   - ✅ Analytics displays
   - ✅ Chatbot responds

---

## 🐛 Step 6: Monitoring & Debugging

### 6.1 View Backend Logs (Render)

1. Go to Render dashboard
2. Click on `orbit-backend` service
3. Click **"Logs"** tab
4. Monitor real-time logs for errors

Common issues:
- **Module not found**: Check `requirements.txt`
- **Port binding error**: Ensure `Procfile` is correct
- **Firebase error**: Verify credentials file uploaded
- **API key error**: Check environment variables

### 6.2 View Frontend Logs (Vercel)

1. Go to Vercel dashboard
2. Click on `orbit-frontend` project
3. Click **"Deployments"** → Select latest deployment
4. Click **"Functions"** tab for function logs
5. Use browser DevTools Console for frontend errors

Common issues:
- **API connection failed**: Verify `VITE_API_URL` is correct
- **CORS error**: Update backend CORS configuration
- **Build failed**: Check `package.json` dependencies
- **Environment variable not found**: Ensure `VITE_` prefix

---

## 🔄 Step 7: Continuous Deployment

### Auto-Deploy on Git Push

Both Vercel and Render are configured for auto-deployment:

1. **Make code changes** locally
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
3. **Push to GitHub**:
   ```bash
   git push orbit_working main
   ```
4. **Automatic deployment**:
   - Vercel: Deploys frontend automatically (~2 min)
   - Render: Deploys backend automatically (~5 min)

### Manual Redeployment

**Vercel (Frontend)**:
1. Go to Vercel dashboard
2. Click project → **"Deployments"**
3. Click **"..."** → **"Redeploy"**

**Render (Backend)**:
1. Go to Render dashboard
2. Click service → **"Manual Deploy"**
3. Click **"Deploy latest commit"**

---

## 📊 Step 8: Custom Domain (Optional)

### Add Custom Domain to Vercel

1. Go to Vercel project
2. Click **"Settings"** → **"Domains"**
3. Click **"Add"**
4. Enter your domain: `orbit.yourdomain.com`
5. Follow DNS configuration instructions
6. Wait for DNS propagation (up to 24 hours)

### Add Custom Domain to Render

1. Go to Render service
2. Click **"Settings"** → **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `api.yourdomain.com`
5. Update DNS records as instructed

### Update Environment Variables

After adding custom domains, update:

**Vercel** (`VITE_API_URL`):
```
VITE_API_URL=https://api.yourdomain.com/api
```

**Backend CORS** (in `app.py`):
```python
origins=["https://orbit.yourdomain.com"]
```

---

## 🚨 Troubleshooting Guide

### Backend Issues

| Issue | Solution |
|-------|----------|
| **500 Internal Server Error** | Check Render logs for Python errors |
| **Module not found** | Add missing package to `requirements.txt` |
| **Firebase authentication failed** | Verify `firebase-credentials.json` uploaded |
| **API key invalid** | Check environment variables in Render |
| **Timeout error** | Increase Render instance size or optimize code |

### Frontend Issues

| Issue | Solution |
|-------|----------|
| **Blank page** | Check browser console for errors |
| **API connection failed** | Verify `VITE_API_URL` in Vercel env vars |
| **CORS error** | Update backend CORS to allow Vercel domain |
| **Build failed** | Check Vercel build logs, verify Node version |
| **Environment variable undefined** | Ensure `VITE_` prefix, redeploy after adding |

### Common Error Messages

**"Cannot read property of undefined"**
- Check API response structure
- Verify frontend is handling null/undefined data

**"Network Error"**
- Backend may be sleeping (Render free tier)
- Check if backend URL is correct
- Verify CORS configuration

**"Firebase: Quota exceeded"**
- Using too many requests on free tier
- Upgrade Firebase plan or optimize queries

---

## 💰 Cost Breakdown

### Free Tier Limits

| Service | Free Tier | Notes |
|---------|-----------|-------|
| **Vercel** | 100 GB bandwidth/month | Unlimited projects |
| **Render** | 750 hours/month | Sleeps after 15 min inactivity |
| **Firebase** | 50k reads, 20k writes/day | Firestore free tier |
| **Gemini API** | 60 requests/minute | Free tier |

### Upgrading for Production

For heavy usage, consider:
- **Vercel Pro**: $20/month (no bandwidth limit)
- **Render Standard**: $7/month (no sleep, faster)
- **Firebase Blaze**: Pay-as-you-go
- **Gemini API**: $0.50/1M tokens (paid tier)

---

## 📱 Step 9: Final Checklist

Before announcing your deployment:

- [ ] Backend health check responds
- [ ] Frontend loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Opportunity search functions
- [ ] Profile creation works
- [ ] AI chatbot responds
- [ ] Analytics dashboard displays data
- [ ] Gamification awards points
- [ ] Application tracker saves data
- [ ] All Firebase collections accessible
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Firebase security rules updated
- [ ] Custom domains configured (if applicable)
- [ ] Monitoring set up

---

## 🎉 Step 10: Go Live!

### Share Your App

Your ORBIT app is now live at:
- **Frontend**: `https://orbit-frontend.vercel.app`
- **Backend API**: `https://orbit-backend.onrender.com/api`

### Monitor Performance

- **Vercel Analytics**: Track page views, performance
- **Render Metrics**: Monitor CPU, memory usage
- **Firebase Console**: Watch database usage

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Vite Documentation](https://vitejs.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🆘 Support

If you encounter issues:

1. Check logs in Render/Vercel dashboards
2. Review this guide's troubleshooting section
3. Verify all environment variables
4. Test API endpoints with Postman/curl
5. Check Firebase quotas and security rules

---

**Deployment Date**: _January 17, 2026_  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

🎯 **You're all set! Your ORBIT application is now deployed and ready for users!**
