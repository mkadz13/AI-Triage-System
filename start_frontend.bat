@echo off
echo Starting Medical Triage System Frontend...
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start the React development server
echo Starting React development server...
npm start

pause

