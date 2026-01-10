# 🔴 ERROR: "Failed to parse resume"

## Why This Happens

The **"Failed to parse resume"** error occurs because:

### ❌ Missing `.env` file with API keys

The backend needs **Gemini API keys** to:
1. Extract information from your PDF resume
2. Structure the data (education, skills, experience)
3. Generate resume grade and evaluation

**Without API keys**, the Gemini API calls fail → Resume parsing fails.

---

## ✅ Solution: Configure API Keys

### Step 1: Create `.env` file

1. Navigate to `backend/` directory
2. Copy `.env.example` to `.env`:
   ```bash
   cd backend
   copy .env.example .env
   ```

### Step 2: Get Gemini API Keys

1. Visit: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"** or **"Create API Key"**
3. Copy your API key

### Step 3: Add Keys to `.env`

Open `backend/.env` and replace the placeholder:

```env
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
GEMINI_API_KEY_2=AIzaSyC...your_actual_key_here
```

**Note:** You can use the same key twice for both variables.

### Step 4: Get Google Search API (for opportunity search)

1. **Search API Key**: https://developers.google.com/custom-search/v1/overview
2. **Search Engine ID**: https://programmablesearchengine.google.com/

Add to `.env`:
```env
GOOGLE_SEARCH_API_KEY=AIzaSyD...your_search_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
```

### Step 5: Restart Backend Server

Close the backend terminal and run again:
```bash
Double-click: start-backend.bat
```

---

## 🔍 How to Verify It's Fixed

After adding API keys:

1. **Check backend logs** - Should see:
   ```
   ✓ Load balancing enabled with 2 Gemini API keys
   ```

2. **Upload resume** - Should see in logs:
   ```
   📄 Parsing resume with Gemini (length: XXXX chars)
   ✓ Gemini responded
   ✓ Successfully parsed resume with content
   ```

3. **Frontend shows** - Resume grade (A+ to C) and evaluation

---

## 🆘 Other Possible Issues

### Issue: "Failed to parse PDF"
**Cause:** PDF file is corrupted or encrypted
**Solution:** Try a different PDF or export a new one

### Issue: Gemini API quota exceeded
**Cause:** Too many API calls (free tier limit)
**Solution:** 
- Wait for quota reset (next day)
- Or create a second API key for load balancing

### Issue: Firebase errors
**Cause:** Missing `firebase-credentials.json`
**Solution:** Download credentials from Firebase Console

---

## 📝 Quick Fix Commands

```bash
# Navigate to backend
cd backend

# Create .env from template
copy .env.example .env

# Edit .env (use notepad or VS Code)
notepad .env

# Restart server
cd ..
start-backend.bat
```

---

## ✅ Checklist

- [ ] Created `backend/.env` file
- [ ] Added `GEMINI_API_KEY` (get from https://makersuite.google.com/app/apikey)
- [ ] Added `GEMINI_API_KEY_2` (can be same as first key)
- [ ] Added `GOOGLE_SEARCH_API_KEY` (optional for search)
- [ ] Added `GOOGLE_SEARCH_ENGINE_ID` (optional for search)
- [ ] Restarted backend server
- [ ] Tested resume upload

---

**Once configured, resume parsing will work perfectly!** ✨
