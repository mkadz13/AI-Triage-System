# Quick Start Guide

## 🚀 Starting the Application

You need to run **TWO** servers: one for the backend (Flask) and one for the frontend (React).

### Step 1: Start the Backend (Flask) - Terminal 1

```bash
# Windows PowerShell
cd C:\Users\Mohammed Kadri\PycharmProjects\TRIAGE

# Activate virtual environment
venv\Scripts\activate

# Start Flask server
python main.py
```

**You should see:**
```
 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

### Step 2: Start the Frontend (React) - Terminal 2

```bash
# Windows PowerShell
cd C:\Users\Mohammed Kadri\PycharmProjects\TRIAGE

# Start React development server
npm start
```

**You should see:**
```
Compiled successfully!
You can now view triage-system-frontend in the browser.
  Local:            http://localhost:3000
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## ✅ Verification

1. **Test Backend API**: Open http://localhost:5000/api/test in your browser
   - Should show: `{"message": "API is working!", "timestamp": "..."}`

2. **Test Frontend**: Open http://localhost:3000
   - Should see the MedTriage homepage

## 🐛 Troubleshooting

### Error: "ECONNREFUSED" or "Proxy error"
- **Solution**: Make sure the Flask backend is running on port 5000
- Check Terminal 1 - you should see Flask server running

### Error: "Port 3000 already in use"
- **Solution**: The React app will automatically use port 3001 (that's fine!)
- Just update the proxy in package.json if needed, or stop the other process

### Backend won't start
- Make sure you're in the virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

## 📝 Important Notes

- **Always start the backend FIRST** before starting the frontend
- Keep both terminal windows open while using the app
- The backend must be running on port 5000 for the frontend to work

