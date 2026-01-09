# 🚀 Quick Start Guide

## Running the Servers

### Option 1: Start Both Servers (Recommended)
Double-click **`start-servers.bat`** in the root directory.

This will:
- Open a new window for the **Backend** (Flask) server on port 5000
- Open a new window for the **Frontend** (Vite) server on port 3000
- Both servers will run independently

### Option 2: Start Servers Individually

**Backend Only:**
- Double-click **`start-backend.bat`**
- Backend runs on: http://localhost:5000

**Frontend Only:**
- Double-click **`start-frontend.bat`**
- Frontend runs on: http://localhost:3000

---

## What Each File Does

| File | Purpose |
|------|---------|
| `start-servers.bat` | Launches both backend and frontend in separate windows |
| `start-backend.bat` | Launches only the Flask backend server |
| `start-frontend.bat` | Launches only the Vite frontend server |

---

## Using the Application

1. **Start the servers** using `start-servers.bat`
2. **Wait** for both servers to fully start (~10-20 seconds)
3. **Open your browser** to http://localhost:3000
4. **Start using Orbit!**

---

## Stopping the Servers

To stop the servers:
- Simply **close** the terminal windows
- Or press **Ctrl+C** in each terminal window

---

## Troubleshooting

### Port Already in Use
If you see "Address already in use" errors:

**Check what's using the port:**
```bash
netstat -ano | findstr :5000  # For backend
netstat -ano | findstr :3000  # For frontend
```

**Kill the process:**
```bash
taskkill /PID <process_id> /F
```

### Backend Won't Start
- Ensure Python is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify `.env` file has Gemini API keys

### Frontend Won't Start
- Ensure Node.js is installed
- Check that dependencies are installed: `cd frontend && npm install`

### Firebase Errors
- Ensure `firebase-credentials.json` exists in the backend directory
- Verify the credentials are valid

---

## Development Workflow

### Making Changes

**Backend Changes:**
- Edit files in `backend/`
- Flask auto-reloads when you save

**Frontend Changes:**
- Edit files in `frontend/src/`
- Vite hot-reloads instantly when you save

### Viewing Logs

**Backend logs** appear in the "Orbit Backend (Flask)" window
**Frontend logs** appear in the "Orbit Frontend (Vite)" window

---

## Alternative: Using VS Code Terminal

If you prefer using VS Code:

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

## Production Deployment

For production, don't use these batch files. Instead:

**Backend:**
- Use a WSGI server like Gunicorn or uWSGI
- Set `FLASK_ENV=production`

**Frontend:**
- Build for production: `npm run build`
- Serve the `dist` folder with a web server

---

## System Requirements

- **Python:** 3.8 or higher
- **Node.js:** 16 or higher
- **npm:** 8 or higher
- **Windows:** 10 or higher (for batch files)

---

## Quick Commands Reference

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install

# Run tests
pytest                    # Backend tests
cd frontend && npm test   # Frontend tests

# Format code
black .                   # Backend formatting
cd frontend && npm run format  # Frontend formatting
```

---

**Need help?** Check the [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions!
