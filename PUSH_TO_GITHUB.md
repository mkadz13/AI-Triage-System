# Complete Guide: Push to GitHub

## Step 1: Verify No Sensitive Files

Run the security check:
```bash
check_before_push.bat
```

Make sure `.env` and `instance/triage.db` are NOT in the list.

## Step 2: Initialize Git (First Time Only)

```bash
# Navigate to your project folder
cd C:\Users\Mohammed Kadri\PycharmProjects\TRIAGE

# Initialize Git repository
git init
```

## Step 3: Stage All Files

```bash
# Add all files (respects .gitignore)
git add .
```

## Step 4: Create Commit (WITH or WITHOUT Custom Date)

### Option A: Commit with Custom Date

```bash
# Set your desired date (YYYY-MM-DD HH:MM:SS)
set GIT_AUTHOR_DATE="2024-01-15 10:30:00"
set GIT_COMMITTER_DATE="2024-01-15 10:30:00"

# Create commit
git commit -m "Initial commit: Medical Triage System"
```

**Or use the batch script:**
```bash
git_commit_with_date.bat "2024-01-15 10:30:00" "Initial commit: Medical Triage System"
```

### Option B: Commit with Current Date (Normal)

```bash
git commit -m "Initial commit: Medical Triage System"
```

## Step 5: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon → **New repository**
3. Repository name: `medical-triage-system` (or your choice)
4. Description: "AI-powered medical triage system with React frontend"
5. Choose **Public** or **Private**
6. **DO NOT** check "Initialize with README" (you already have one)
7. Click **Create repository**

## Step 6: Connect Local Repository to GitHub

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/medical-triage-system.git
```

## Step 7: Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 8: Verify on GitHub

Go to your repository on GitHub and verify all files are there (except `.env` and database files).

---

## Modifying Commit Date

### If You Haven't Pushed Yet:

```bash
# Set new date
set GIT_AUTHOR_DATE="2024-01-15 10:30:00"
set GIT_COMMITTER_DATE="2024-01-15 10:30:00"

# Amend the commit
git commit --amend --no-edit

# Then push normally
git push
```

### If You Already Pushed:

```bash
# Set new date
set GIT_AUTHOR_DATE="2024-01-15 10:30:00"
set GIT_COMMITTER_DATE="2024-01-15 10:30:00"

# Amend the commit
git commit --amend --no-edit

# Force push (rewrites history on GitHub)
git push --force-with-lease
```

**⚠️ Warning**: Force push rewrites history. Only use on your own repositories!

---

## Quick Reference: Date Format

```
"YYYY-MM-DD HH:MM:SS"
```

Examples:
- `"2024-01-15 10:30:00"` - January 15, 2024 at 10:30 AM
- `"2024-12-25 14:00:00"` - December 25, 2024 at 2:00 PM
- `"2023-06-01 09:15:30"` - June 1, 2023 at 9:15:30 AM

---

## Complete Example (With Custom Date)

```bash
# 1. Check security
check_before_push.bat

# 2. Initialize (if first time)
git init

# 3. Stage files
git add .

# 4. Commit with custom date
set GIT_AUTHOR_DATE="2024-01-15 10:30:00"
set GIT_COMMITTER_DATE="2024-01-15 10:30:00"
git commit -m "Initial commit: Medical Triage System"

# 5. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/medical-triage-system.git

# 6. Push
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "Repository not found"
- Check your GitHub username is correct
- Make sure you created the repository on GitHub first

### "Permission denied"
- Make sure you're logged into GitHub
- You may need to use GitHub Personal Access Token instead of password

### "Everything up-to-date" but nothing on GitHub
- Check if you're on the right branch: `git branch`
- Make sure you ran `git push -u origin main`

### Want to change date after pushing?
- Use `git push --force-with-lease` (only if you're the only one using the repo)

