# Quick Deployment Commands

## 1️⃣ Push to GitHub
```bash
cd C:\Users\JAYAN\Downloads\orbit
git init
git add .
git commit -m "Ready for deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/orbit.git
git branch -M main
git push -u origin main
```

## 2️⃣ Deploy Backend (Render)
1. Go to https://dashboard.render.com/
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
5. Add environment variables (see DEPLOYMENT.md)
6. Add Firebase JSON as Secret File
7. Deploy!

## 3️⃣ Deploy Frontend (Vercel)
1. Go to https://vercel.com/dashboard
2. New Project → Import from GitHub
3. Settings:
   - Root Directory: `frontend`
   - Framework: Vite
   - Build: `npm run build`
   - Output: `dist`
4. Add environment variable:
   ```
   VITE_API_URL=https://your-render-url.onrender.com/api
   ```
5. Deploy!

## 4️⃣ Update CORS
Update backend URL in Render environment variables:
```
ALLOWED_ORIGINS=https://your-vercel-url.vercel.app
```

## ✅ Done!
Visit your Vercel URL and test the app!

See DEPLOYMENT.md for detailed instructions.
