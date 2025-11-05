@echo off
echo ========================================
echo Pre-Push Security Check
echo ========================================
echo.

echo Checking for sensitive files...
echo.

REM Check for .env file
if exist .env (
    echo [ERROR] .env file found! DO NOT COMMIT THIS!
    echo Remove it from staging: git reset .env
    echo.
) else (
    echo [OK] No .env file found
)

REM Check for database files
if exist instance\triage.db (
    echo [WARNING] Database file found (instance\triage.db)
    echo Make sure this is in .gitignore
    echo.
) else (
    echo [OK] No database file found
)

REM Check for venv folder
if exist venv (
    echo [OK] venv folder found (should be gitignored)
) else (
    echo [OK] No venv folder
)

REM Check for node_modules
if exist node_modules (
    echo [OK] node_modules folder found (should be gitignored)
) else (
    echo [OK] No node_modules folder
)

echo.
echo ========================================
echo Checking git status...
echo ========================================
echo.

git status --short

echo.
echo ========================================
echo Checking for sensitive patterns in staged files...
echo ========================================
echo.

git diff --cached --name-only | findstr /i "\.env triage.db venv node_modules" >nul
if %errorlevel% == 0 (
    echo [ERROR] Sensitive files detected in staging area!
    echo Review what you're about to commit!
) else (
    echo [OK] No obvious sensitive files in staging area
)

echo.
echo ========================================
echo Final Checklist:
echo ========================================
echo [ ] .env is NOT in git status
echo [ ] instance/triage.db is NOT in git status
echo [ ] venv/ is NOT in git status
echo [ ] node_modules/ is NOT in git status
echo [ ] All sensitive data is in .env (gitignored)
echo.
echo If all checks pass, you're safe to commit!
echo.
pause

