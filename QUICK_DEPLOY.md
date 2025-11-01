# 🚀 Quick Deploy to Render (5 Minutes)

## ✅ Prerequisites
- GitHub account
- Your bot code (already done!)

---

## 📋 Step-by-Step Guide

### Step 1: Push to GitHub (2 minutes)

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create a new repository on GitHub
# Go to: https://github.com/new
# Repository name: kakinada-legal-bot
# Keep it Private or Public (your choice)
# Click "Create repository"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/kakinada-legal-bot.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy on Render (3 minutes)

1. **Go to Render**: https://render.com

2. **Sign Up**:
   - Click "Get Started for Free"
   - Sign up with your GitHub account
   - Authorize Render to access your repositories

3. **Create New Service**:
   - Click "New +" in the top right
   - Select "Background Worker"

4. **Connect Repository**:
   - Select "kakinada-legal-bot" from the list
   - Click "Connect"

5. **Configure Settings**:
   ```
   Name: kakinada-legal-bot
   Environment: Python 3
   Region: Singapore (closest to India)
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   Instance Type: Free
   ```

6. **Click "Create Background Worker"**

7. **Wait 2-3 minutes** for deployment

8. **Check Logs**:
   - You should see:
   ```
   ✅ Gemini model with Google Search initialized successfully
   🚀 Kakinada Legal Assistant Bot is starting...
   Application started
   ```

---

### Step 3: Test Your Bot

1. Open Telegram
2. Search for: `@ai_governance_bot`
3. Send `/start`
4. Try all commands!

---

## 🎉 That's It!

Your bot is now running 24/7 for FREE! 🚀

### What Render Free Tier Gives You:
- ✅ **750 Free instance hours/month** (enough for 24/7: 31 days × 24 hours = 744 hours)
- ✅ Auto-restart if bot crashes
- ✅ Auto-deploy on git push
- ✅ Real-time logs
- ✅ No credit card needed

### ⚠️ Important Render Free Tier Limitations:

**1. Spin Down on Idle (Web Services Only)**
- If you deployed as a **Web Service**, it spins down after 15 minutes of inactivity
- Spins back up when receiving a request (takes ~30-60 seconds)
- **Solution**: Deploy as a **Background Worker** instead (doesn't spin down!)

**2. Monthly Limits**
- 750 Free instance hours per workspace
- Outbound bandwidth limits apply
- If exceeded, service suspends until next month

**3. Service May Restart**
- Render might restart your service at any time
- Your bot will automatically reconnect when this happens

**4. No Persistent Disk**
- PDFs are generated temporarily (sent to user immediately)
- No permanent file storage on free tier

---

## 📊 Monitor Your Bot

### View Logs:
1. Go to: https://dashboard.render.com
2. Click on your service
3. Click "Logs" tab
4. See real-time output

### Check Status:
- Green dot = Running ✅
- Red dot = Error ❌

### Restart Bot:
1. Click "Manual Deploy"
2. Select "Clear build cache & deploy"

---

## 🔄 Update Your Bot

When you make changes to code:

```bash
# Make your changes in the code
# Then:

git add .
git commit -m "Updated bot features"
git push

# Render will automatically deploy the new version!
```

---

## 🆘 Troubleshooting

### Bot Not Starting?

**Check 1: View Logs**
- Go to Render dashboard
- Click "Logs"
- Look for errors

**Check 2: Verify Build**
- Make sure `requirements.txt` is correct
- Check if all dependencies installed

**Check 3: Test Locally First**
```bash
python bot.py
```

### Bot Keeps Restarting?

**Possible Causes**:
1. API keys invalid → Check config.py
2. Memory limit reached → Upgrade plan (unlikely for free tier)
3. Code error → Check logs for traceback

---

## 💡 Tips

### Keep Bot Running:
- Render free tier gives 750 hours/month
- This is enough for 24/7 operation
- No action needed!

### Get Notified:
1. Go to Render dashboard
2. Settings → Notifications
3. Add your email
4. Get alerts when bot goes down

### View Metrics:
- Dashboard shows CPU, Memory usage
- Free tier: 512MB RAM, 0.1 CPU
- Enough for this bot!

---

## 🚀 Alternative: Deploy to Railway

If you prefer Railway:

1. Go to: https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub"
4. Select your repository
5. Click "Deploy"
6. Done! (Railway gives $5 free credit/month)

---

## 📞 Need Help?

Common Issues:

**"Build Failed"**
→ Check requirements.txt has all dependencies

**"Application Error"**
→ Check logs for Python errors

**"No such file"**
→ Make sure all files are pushed to GitHub

**"API Key Error"**
→ Verify keys in config.py are correct

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] requirements.txt is complete
- [ ] Bot works locally (tested with `python bot.py`)
- [ ] All API keys are in config.py
- [ ] No syntax errors

After deploying:
- [ ] Check logs on Render
- [ ] Test bot on Telegram
- [ ] All commands working
- [ ] PDF generation works
- [ ] Location sharing works

---

## 🎯 Next Steps

After successful deployment:

1. **Share your bot**: Give the link to users
2. **Monitor usage**: Check logs daily for first week
3. **Gather feedback**: Ask users for improvements
4. **Update regularly**: Push updates via GitHub

---

## 💰 When to Upgrade?

Stick with **FREE** plan if:
- ✅ Bot handles < 100 users/day
- ✅ Response time is acceptable
- ✅ No downtime issues

Upgrade to **$7/month** if:
- ❌ Bot becomes slow
- ❌ Memory errors in logs
- ❌ Many users (500+/day)

---

**Made with ❤️ for Kakinada Legal Assistant Bot**

🎉 Congratulations on deploying your bot! 🎉

