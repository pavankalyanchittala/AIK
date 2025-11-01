# 🔐 Environment Variables Setup Guide

## 📋 Overview

This bot uses **environment variables** to store sensitive API keys securely. This prevents accidental exposure of keys when pushing to GitHub.

---

## 🏠 Local Development Setup

### Step 1: Create `.env` File

Create a file named `.env` in the project root directory (`C:\Users\pavan\OneDrive\Desktop\AIK\.env`)

**Windows (PowerShell):**
```powershell
cd C:\Users\pavan\OneDrive\Desktop\AIK
notepad .env
```

**Linux/Mac:**
```bash
cd /path/to/AIK
nano .env
```

### Step 2: Add Your API Keys

Copy and paste this into your `.env` file:

```env
# Kakinada Legal Assistant Bot - API Keys
# IMPORTANT: Never commit this file to GitHub!

# Telegram Bot API Key
TELEGRAM_BOT_TOKEN=8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk

# Google Gemini API Key (NEW - NOT LEAKED)
GEMINI_API_KEY=AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8

# Google Maps API Key
GOOGLE_MAPS_API_KEY=AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
```

### Step 3: Save and Test

1. **Save the file** (Ctrl+S in Notepad)
2. **Close the file**
3. **Restart the bot:**
   ```powershell
   python bot.py
   ```

The bot will now load keys from `.env` file! ✅

---

## 🚀 Deployment Setup

### For Render (Recommended)

**DO NOT** create a `.env` file on Render. Instead, add environment variables in the dashboard:

#### Step 1: Open Environment Settings
1. Go to Render Dashboard
2. Select your service
3. Click "Environment" tab on the left

#### Step 2: Add Variables
Click "Add Environment Variable" and add these **3 variables**:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | `8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk` |
| `GEMINI_API_KEY` | `AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8` |
| `GOOGLE_MAPS_API_KEY` | `AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ` |

#### Step 3: Save and Redeploy
1. Click "Save Changes"
2. Render will automatically redeploy with new keys ✅

---

### For Railway

#### Step 1: Open Variables Tab
1. Go to Railway Dashboard
2. Select your service
3. Click "Variables" tab

#### Step 2: Add Raw Editor
Click "RAW Editor" and paste:

```
TELEGRAM_BOT_TOKEN=8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk
GEMINI_API_KEY=AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8
GOOGLE_MAPS_API_KEY=AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
```

#### Step 3: Deploy
Railway will automatically redeploy ✅

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Keep `.env` file in `.gitignore` (already done!)
- ✅ Use environment variables on deployment platforms
- ✅ Rotate API keys if leaked
- ✅ Use different keys for development and production

### ❌ DON'T:
- ❌ Commit `.env` file to GitHub
- ❌ Share `.env` file publicly
- ❌ Post API keys in screenshots
- ❌ Hardcode keys in source files (for production)

---

## 🔄 How It Works

### Priority Order:

```
1. Environment Variable (.env file or platform)
   ⬇️
2. Fallback to hardcoded value in config.py (for convenience)
```

### In `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

# Try environment variable first, fallback to hardcoded
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8")
```

---

## 🧪 Testing

### Test if .env is loaded:
```python
import os
from dotenv import load_dotenv

load_dotenv()
print("Telegram Token:", os.getenv("TELEGRAM_BOT_TOKEN", "NOT FOUND"))
print("Gemini Key:", os.getenv("GEMINI_API_KEY", "NOT FOUND"))
print("Maps Key:", os.getenv("GOOGLE_MAPS_API_KEY", "NOT FOUND"))
```

### Expected Output:
```
Telegram Token: 8187667435:AAER2q...
Gemini Key: AIzaSyB8EG93ctL...
Maps Key: AIzaSyDE9Rj-dBn...
```

---

## 🆘 Troubleshooting

### ".env file not found"
**Solution:** Make sure `.env` is in the same directory as `bot.py`

### "Keys not loading"
**Solution:** 
1. Check `.env` file has no spaces around `=`
   ```
   GOOD: GEMINI_API_KEY=AIzaSyB...
   BAD:  GEMINI_API_KEY = AIzaSyB...
   ```
2. Check no quotes around values
   ```
   GOOD: GEMINI_API_KEY=AIzaSyB...
   BAD:  GEMINI_API_KEY="AIzaSyB..."
   ```

### "Still getting 403 error"
**Solution:** The new Gemini key might also be restricted. Get another one from:
https://aistudio.google.com/apikey

### "Bot works locally but not on Render"
**Solution:** 
1. Make sure environment variables are set in Render Dashboard
2. Check spelling of variable names (case-sensitive!)
3. Redeploy after adding variables

---

## 📝 Quick Reference

### Your Current API Keys:

```
Telegram Bot Token: 8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk
Gemini API Key:     AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8
Google Maps Key:    AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
```

### Where to Get New Keys:

| Service | URL |
|---------|-----|
| **Telegram Bot** | https://t.me/BotFather |
| **Gemini API** | https://aistudio.google.com/apikey |
| **Google Maps** | https://console.cloud.google.com/apis/credentials |

---

## 🎯 For GitHub (Public Repo)

If you plan to push to public GitHub:

### Step 1: Clean config.py
Remove hardcoded keys from `config.py`:

```python
# Before deploying to public GitHub, change fallbacks to None:
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Remove default
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Remove default
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Remove default
```

### Step 2: Document in README
Add to README:
```markdown
## Setup
1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Run `python bot.py`
```

### Step 3: Create .env.example
```env
TELEGRAM_BOT_TOKEN=your_telegram_token_here
GEMINI_API_KEY=your_gemini_key_here
GOOGLE_MAPS_API_KEY=your_maps_key_here
```

**For now**, since you're just deploying (not making public repo), the current setup with fallbacks is fine!

---

## ✅ Final Checklist

For Local Development:
- [ ] `.env` file created in project root
- [ ] All 3 API keys added to `.env`
- [ ] `.env` is in `.gitignore` (already done!)
- [ ] Bot runs without errors: `python bot.py`
- [ ] Test `/start` command works

For Deployment (Render/Railway):
- [ ] Environment variables added in dashboard
- [ ] All 3 variables: `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, `GOOGLE_MAPS_API_KEY`
- [ ] Service redeployed after adding variables
- [ ] Logs show no API key errors
- [ ] Bot responds to commands

---

**Last Updated**: November 2025  
**Your New Gemini Key**: `AIzaSyB8EG93ctLYzuu2J07TtilNEX4L1BWVOW8` ✅  
**Status**: Not leaked, ready to use!

**Made with ❤️ for Kakinada Legal Assistant Bot**

