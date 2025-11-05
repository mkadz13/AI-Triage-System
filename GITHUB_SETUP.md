# GitHub Setup Guide

## ✅ Pre-Push Checklist

Before pushing to GitHub, make sure you've:

1. ✅ Created `.gitignore` (already done)
2. ✅ No `.env` file in the repository
3. ✅ No database files (`instance/triage.db`) committed
4. ✅ No `venv/` folder committed
5. ✅ No `node_modules/` folder committed
6. ✅ All secrets are in `.env` (which is gitignored)

## 🔐 What Will Be Public

### ✅ Safe to Commit:
- `main.py` (backend code)
- `requirements.txt`
- `package.json`
- `src/` (React frontend code)
- `public/` (public assets)
- `README.md`
- `env_template.txt` (template only, no real keys)
- Configuration files (tailwind.config.js, etc.)

### ❌ NEVER Commit:
- `.env` (contains your API keys!)
- `instance/triage.db` (database with patient data!)
- `venv/` (virtual environment)
- `node_modules/` (can be reinstalled)
- Any file with real API keys or secrets

## 📝 Steps to Push to GitHub

### 1. Initialize Git (if not already done)
```bash
git init
```

### 2. Verify .gitignore is working
```bash
# Check what will be committed
git status

# Should NOT see:
# - .env
# - instance/triage.db
# - venv/
# - node_modules/
```

### 3. Add all files
```bash
git add .
```

### 4. Verify sensitive files are NOT included
```bash
git status

# Double-check that .env and instance/ are NOT listed!
```

### 5. Create initial commit
```bash
git commit -m "Initial commit: Medical Triage System with React frontend"
```

### 6. Create GitHub Repository
1. Go to GitHub.com
2. Click "New repository"
3. Name it: `medical-triage-system` (or your preferred name)
4. **DO NOT** initialize with README (you already have one)
5. Click "Create repository"

### 7. Connect and Push
```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/medical-triage-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🔍 Double-Check Before Pushing

Run this command to see what will be committed:
```bash
git ls-files | grep -E "(\.env|triage\.db|venv|node_modules)"
```

**If this shows ANY files, STOP and check your .gitignore!**

## 🛡️ Security Best Practices

### After Pushing:
1. **Never commit `.env` files** - Always use environment variables
2. **Rotate API keys** if you accidentally committed them:
   - Generate new OpenAI API key
   - Update `.env` locally
3. **Review your repository** after pushing:
   - Go to your GitHub repo
   - Check if any sensitive files are visible
   - If found, remove them immediately (they're in Git history!)

### For Collaborators:
- Share `env_template.txt` as reference
- Each developer creates their own `.env` file locally
- Never share `.env` files via chat/email

## 📋 What to Include in README

Your README should mention:
- "Copy `env_template.txt` to `.env` and fill in your API keys"
- "Never commit `.env` files"
- "Create your own `.env` file locally"

## 🚨 If You Accidentally Committed Secrets

### Immediate Actions:
1. **Rotate ALL exposed keys immediately**
2. **Remove from Git history** (advanced - use git filter-branch or BFG Repo-Cleaner)
3. **Or create a new repository** and start fresh

### Prevention:
- Use `git status` before every commit
- Review what files are being added
- When in doubt, don't commit!

