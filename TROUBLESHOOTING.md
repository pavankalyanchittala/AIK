# 🔧 Troubleshooting Guide - Kakinada Legal Assistant Bot

## ❌ Common Errors and Solutions

---

## 1. 🔴 "Conflict: terminated by other getUpdates request"

### Error Message:
```
telegram.error.Conflict: Conflict: terminated by other getUpdates request; 
make sure that only one bot instance is running
```

### ⚠️ Cause:
**Multiple instances of the bot are running simultaneously.** Telegram doesn't allow this because only one instance can poll for updates at a time.

### ✅ Solution (Windows):

#### Step 1: Kill All Running Instances
```powershell
# Find all Python processes
tasklist /FI "IMAGENAME eq python.exe"

# Kill all Python processes (careful if you're running other Python apps!)
taskkill /F /IM python.exe

# Or kill specific process by PID
taskkill /F /PID <PID_NUMBER>
```

#### Step 2: Start Fresh Instance
```powershell
cd C:\Users\pavan\OneDrive\Desktop\AIK
python bot.py
```

### ✅ Solution (Linux/Mac):

#### Step 1: Kill All Running Instances
```bash
# Find bot processes
ps aux | grep bot.py

# Kill all bot instances
pkill -f bot.py

# Or kill specific process
kill <PID>
```

#### Step 2: Start Fresh Instance
```bash
cd /path/to/AIK
python bot.py
```

### 🔒 Prevention:
- **Always use ONE terminal** to run the bot
- **Check for existing processes** before starting
- **Use Ctrl+C** to stop (don't just close terminal)
- **On deployment**: Platform handles this automatically

---

## 2. 🔴 Bot Starts But Doesn't Respond

### Symptoms:
- Bot shows "Application started"
- No response to `/start` or other commands
- No errors in logs

### Possible Causes & Solutions:

#### A. Wrong Telegram Token
```python
# Check config.py
TELEGRAM_BOT_TOKEN = "8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk"
```

**Test Token:**
```bash
curl https://api.telegram.org/bot8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk/getMe
```

#### B. Bot is Banned/Deleted
- Check @BotFather on Telegram
- Verify bot still exists
- Check if bot was accidentally deleted

#### C. Network/Firewall Issues
```bash
# Test Telegram API connectivity
curl https://api.telegram.org/

# Test with ping
ping api.telegram.org
```

---

## 3. 🔴 "404 models/gemini-1.5-flash-latest is not found"

### Error Message:
```
google.genai.errors.ClientError: 404 models/gemini-1.5-flash-latest is not found
```

### ✅ Solution:
The model name changed. Update to use `gemini-flash-lite-latest`:

```python
# In config.py - Already fixed!
MODEL_NAME = "gemini-flash-lite-latest"
```

---

## 4. 🔴 "google_search_retrieval is not supported"

### Error Message:
```
400 google_search_retrieval is not supported. 
Please use google_search tool instead.
```

### ✅ Solution:
API changed. Now using correct syntax:

```python
# Already fixed in bot.py!
tools=[types.Tool(googleSearch=types.GoogleSearch())]
```

---

## 5. 🔴 PDF Generation Fails

### Symptoms:
- Error when generating complaint/FIR
- "Failed to generate PDF" message
- Missing fonts

### Solutions:

#### A. Check reportlab Installation
```bash
pip install --upgrade reportlab
```

#### B. Verify Fonts
```python
# Already handled in pdf_generator.py
# Uses built-in Helvetica font
```

#### C. Test PDF Generation Locally
```python
from pdf_generator import PDFGenerator

pdf_gen = PDFGenerator()
test_data = {
    'full_name': 'Test User',
    'address': 'Test Address',
    'incident_details': 'Test incident'
}
pdf_gen.generate_complaint_form(test_data, 'test.pdf')
```

---

## 6. 🔴 Location/Police Station Not Working

### Symptoms:
- Wrong police stations suggested
- "No police stations found"
- Location not detected

### Solutions:

#### A. Check Google Maps API Key
```python
# In config.py
GOOGLE_MAPS_API_KEY = "AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ"
```

**Test API Key:**
```bash
curl "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=16.9891,82.2475&radius=5000&type=police&key=AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ"
```

#### B. Verify API is Enabled
1. Go to: https://console.cloud.google.com/
2. Enable: **Places API**
3. Enable: **Geocoding API**
4. Check quota limits

#### C. User Not Sharing Location Properly
- User must click "Share Location" button in Telegram
- GPS must be enabled on their device
- Telegram must have location permissions

---

## 7. 🔴 "ModuleNotFoundError: No module named 'X'"

### Error Message:
```
ModuleNotFoundError: No module named 'google.genai'
```

### ✅ Solution:
```bash
# Reinstall all dependencies
pip install -r requirements.txt

# Or install specific module
pip install google-genai
```

---

## 8. 🔴 Deployment Issues on Render

### A. Build Failed

**Error**: "Build failed" on Render

**Solutions:**
1. Check `requirements.txt` exists
2. Verify `runtime.txt` has correct Python version
3. Check build logs for specific error
4. Ensure all files are pushed to GitHub

```bash
# Verify files exist
ls -la requirements.txt runtime.txt Procfile

# Check git status
git status

# Push missing files
git add .
git commit -m "Add deployment files"
git push
```

### B. Bot Spins Down After 15 Minutes

**Symptom**: Bot stops responding after inactivity

**Cause**: Deployed as "Web Service" instead of "Background Worker"

**Solution:**
1. Delete current service on Render
2. Create new service as **"Background Worker"** ⚠️
3. Redeploy

### C. Service Suspended

**Error**: "Service suspended" on Render dashboard

**Causes & Solutions:**

1. **Exceeded 750 Free Hours**
   - Wait until 1st of next month (hours reset)
   - Or upgrade to paid plan ($7/month)

2. **Exceeded Bandwidth**
   - Add payment method
   - Or wait until next month

3. **High Service-Initiated Traffic**
   - Upgrade to paid plan
   - Optimize API calls

**Check Usage:**
- Dashboard → Billing → "Monthly Included Usage"

---

## 9. 🔴 Bot Slow to Respond

### Symptoms:
- Takes 10-30 seconds to respond
- Timeout errors
- Users complain about delays

### Solutions:

#### A. Optimize Gemini API Calls
```python
# Already optimized in bot.py
# Uses gemini-flash-lite-latest (fastest model)
# Streams responses for better UX
```

#### B. Optimize Google Maps Calls
```python
# Already optimized
# Caches nearby police stations
# Uses radius search (faster than text search)
```

#### C. Check Internet Connection
```bash
# Test API latency
curl -w "@curl-format.txt" -o /dev/null -s https://api.telegram.org/
```

#### D. Upgrade Deployment Plan
- Free tier: Shared resources
- Paid tier: Dedicated resources (faster)

---

## 10. 🔴 Environment Variable Issues

### Symptoms:
- API keys not found
- "None" values in config
- Import errors

### Solutions:

#### A. Check .env File (Local Development)
```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk
GEMINI_API_KEY=AIzaSyC1DRSmrGVvxMzARHhsLWTqiwpSVPLEOmI
GOOGLE_MAPS_API_KEY=AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
EOF
```

#### B. Check Environment Variables (Render)
1. Dashboard → Service → Environment
2. Add each variable:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
   - `GOOGLE_MAPS_API_KEY`
3. Save and redeploy

#### C. Verify Loading in Code
```python
# In config.py - Already handled!
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'default_value')
```

---

## 🔍 Debugging Tools

### 1. Check Bot Status
```python
import asyncio
from telegram import Bot

async def test_bot():
    bot = Bot(token="YOUR_TOKEN")
    me = await bot.get_me()
    print(f"Bot: {me.first_name} (@{me.username})")
    print(f"ID: {me.id}")

asyncio.run(test_bot())
```

### 2. Test Gemini API
```python
from google import genai

client = genai.Client(api_key="YOUR_GEMINI_KEY")
response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents="Say hello"
)
print(response.text)
```

### 3. Test Google Maps API
```python
import googlemaps

gmaps = googlemaps.Client(key="YOUR_MAPS_KEY")
result = gmaps.places_nearby(
    location=(16.9891, 82.2475),
    radius=5000,
    type='police'
)
print(f"Found {len(result['results'])} police stations")
```

### 4. Check All Dependencies
```bash
pip list | grep -E "telegram|google|reportlab|dotenv|pillow"
```

### 5. Enable Debug Logging
```python
# Add to bot.py (temporarily)
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change from INFO to DEBUG
)
```

---

## 📊 Monitoring & Logs

### Local Development:
```bash
# Run with verbose logging
python bot.py 2>&1 | tee bot.log

# Monitor log file
tail -f bot.log
```

### On Render:
1. Dashboard → Service → Logs
2. Enable "Live Logs" toggle
3. Download logs for analysis

### On Railway:
1. Dashboard → Deployment → Logs
2. Real-time streaming enabled by default

---

## 🆘 When All Else Fails

### 1. Fresh Start
```bash
# Delete and recreate virtual environment
rm -rf venv/
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Test
python bot.py
```

### 2. Verify All API Keys
- Telegram: https://t.me/BotFather
- Gemini: https://ai.google.dev/
- Google Maps: https://console.cloud.google.com/

### 3. Check for Updates
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Check for security issues
pip check
```

### 4. Test Each Component Individually
```bash
# Test imports
python -c "import telegram; print('Telegram OK')"
python -c "from google import genai; print('Gemini OK')"
python -c "import googlemaps; print('Maps OK')"
python -c "from reportlab.pdfgen import canvas; print('PDF OK')"
```

---

## 📞 Get Help

### Before Asking for Help, Provide:

1. **Error Message** (full traceback)
2. **What you tried** (steps taken)
3. **Environment**:
   - OS: Windows/Linux/Mac
   - Python version: `python --version`
   - Package versions: `pip list`
4. **Logs** (last 50 lines)
5. **Config** (without sensitive keys!)

### Useful Resources:

- **Telegram Bot API**: https://core.telegram.org/bots/api
- **python-telegram-bot Docs**: https://docs.python-telegram-bot.org/
- **Gemini API Docs**: https://ai.google.dev/docs
- **Google Maps API**: https://developers.google.com/maps
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app/

---

## ✅ Quick Checklist

Before running the bot:
- [ ] Python 3.10+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys configured in `config.py`
- [ ] No other bot instances running
- [ ] Internet connection active
- [ ] Telegram accessible

After deployment:
- [ ] Service deployed as "Background Worker"
- [ ] Environment variables set
- [ ] Service status: "Active"
- [ ] Logs show "Application started"
- [ ] Bot responds to `/start`
- [ ] All commands working

---

**Last Updated**: November 2025  
**Bot Version**: 1.0  
**Compatibility**: Windows/Linux/Mac

**Made with ❤️ for Kakinada Legal Assistant Bot**

