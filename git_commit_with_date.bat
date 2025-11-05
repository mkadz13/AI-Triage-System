@echo off
REM Git commit with custom date
REM Usage: git_commit_with_date.bat "YYYY-MM-DD HH:MM:SS" "commit message"
REM Example: git_commit_with_date.bat "2024-01-15 10:30:00" "Initial commit"

if "%1"=="" (
    echo Usage: git_commit_with_date.bat "YYYY-MM-DD HH:MM:SS" "commit message"
    echo Example: git_commit_with_date.bat "2024-01-15 10:30:00" "Initial commit"
    exit /b 1
)

if "%2"=="" (
    echo Usage: git_commit_with_date.bat "YYYY-MM-DD HH:MM:SS" "commit message"
    echo Example: git_commit_with_date.bat "2024-01-15 10:30:00" "Initial commit"
    exit /b 1
)

set CUSTOM_DATE=%1
set COMMIT_MESSAGE=%2

echo Setting commit date to: %CUSTOM_DATE%
echo Commit message: %COMMIT_MESSAGE%
echo.

REM Set the date for both author and committer
set GIT_AUTHOR_DATE=%CUSTOM_DATE%
set GIT_COMMITTER_DATE=%CUSTOM_DATE%

REM Stage all changes first
git add .

REM Commit with custom date
git commit -m "%COMMIT_MESSAGE%"

echo.
echo Commit created with custom date: %CUSTOM_DATE%
echo You can now push with: git push

