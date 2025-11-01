# 🚀 Deployment Guide - Run Bot 24/7

## 📋 Table of Contents
1. [Free Deployment Options](#free-options)
2. [Paid Deployment Options](#paid-options)
3. [Quick Deploy to Render (Recommended)](#render-deployment)
4. [Deploy to Railway](#railway-deployment)
5. [Deploy to PythonAnywhere](#pythonanywhere-deployment)
6. [Deploy to AWS EC2](#aws-deployment)
7. [Deploy to VPS (DigitalOcean/Linode)](#vps-deployment)

---

## 🆓 Free Deployment Options

### Best Free Options (Recommended)
1. **Render** - 750 hours/month free (enough for 24/7)
2. **Railway** - $5 free credit/month (runs ~1 month 24/7)
3. **PythonAnywhere** - Free tier with always-on tasks
4. **Fly.io** - Free tier with 3 shared VMs

---

## 💰 Paid Deployment Options

### Budget-Friendly ($3-10/month)
1. **DigitalOcean** - $4/month VPS
2. **Linode** - $5/month VPS
3. **AWS Lightsail** - $3.50/month VPS
4. **Vultr** - $2.50/month VPS

### Premium ($10+/month)
1. **AWS EC2** - Full control, scalable
2. **Google Cloud** - Similar to AWS
3. **Azure** - Enterprise-grade

---

## 🎯 Render Deployment (RECOMMENDED - FREE)

### Why Render?
✅ Free 750 hours/month (24/7 coverage)
✅ Easy setup (5 minutes)
✅ Auto-deploy on git push
✅ HTTPS/SSL included
✅ No credit card required

### Step-by-Step Instructions:

#### 1. Prepare Your Code

First, create a startup script:

```bash
# Create start.sh
echo '#!/bin/bash
python bot.py' > start.sh

# Make it executable (Linux/Mac)
chmod +x start.sh
```

For Windows (create `start.bat`):
```batch
@echo off
python bot.py
```

#### 2. Create Render Account

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub/GitLab/Email

#### 3. Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for deployment"

# Create GitHub repo and push
# Follow GitHub instructions to push
```

#### 4. Deploy on Render

1. **Login to Render Dashboard**
2. **Click "New +"** → Select "Background Worker"
3. **Connect GitHub Repository**
   - Authorize Render to access your GitHub
   - Select your bot repository

4. **Configure Service:**
   ```
   Name: kakinada-legal-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```

5. **Add Environment Variables** (Optional - if you move API keys):
   ```
   TELEGRAM_BOT_TOKEN = 8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk
   GEMINI_API_KEY = AIzaSyC1DRSmrGVvxMzARHhsLWTqiwpSVPLEOmI
   GOOGLE_MAPS_API_KEY = AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
   ```

6. **Click "Create Background Worker"**

7. **Wait 2-5 minutes** - Render will:
   - Clone your repo
   - Install dependencies
   - Start your bot

8. **Check Logs** - You should see:
   ```
   ✅ Gemini model with Google Search initialized successfully
   🚀 Kakinada Legal Assistant Bot is starting...
   ```

#### 5. Monitor Your Bot

- **Dashboard**: https://dashboard.render.com
- **Logs**: View real-time logs
- **Metrics**: CPU, Memory usage
- **Auto-restart**: Render auto-restarts if bot crashes

---

## 🚂 Railway Deployment (FREE $5/month credit)

### Step-by-Step:

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub**
4. **Select your repository**
5. **Settings**:
   ```
   Start Command: python bot.py
   ```
6. **Deploy** → Bot will be live in 2-3 minutes

**Note**: $5 free credit = ~30 days of 24/7 operation

---

## 🐍 PythonAnywhere Deployment (FREE)

### Step-by-Step:

1. **Sign up**: https://www.pythonanywhere.com
2. **Upload your code**:
   - Use "Files" tab to upload all files
   - Or use git clone

3. **Install Dependencies**:
   ```bash
   # Open Bash console
   pip3.10 install --user -r requirements.txt
   ```

4. **Create Always-On Task**:
   - Go to "Tasks" tab
   - Add: `python3.10 /home/yourusername/bot.py`
   - Set as "Always-on"

5. **Start Bot** - Bot will run 24/7

**Limitations**:
- Free tier: Limited CPU
- May be slower than Render
- Good for basic bots

---

## ☁️ AWS EC2 Deployment (Paid - Full Control)

### Cost: ~$3.50/month (t2.micro)

### Step-by-Step:

1. **Create AWS Account**: https://aws.amazon.com

2. **Launch EC2 Instance**:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (free tier eligible)
   - Storage: 8GB
   - Security Group: Allow SSH (port 22)

3. **Connect via SSH**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

4. **Setup Environment**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3 python3-pip git -y

   # Clone your repository
   git clone https://github.com/yourusername/kakinada-legal-bot.git
   cd kakinada-legal-bot

   # Install dependencies
   pip3 install -r requirements.txt
   ```

5. **Run Bot with PM2 (Process Manager)**:
   ```bash
   # Install PM2
   sudo apt install npm -y
   sudo npm install -g pm2

   # Start bot
   pm2 start bot.py --interpreter python3 --name legal-bot

   # Enable auto-start on reboot
   pm2 startup
   pm2 save
   ```

6. **Check Status**:
   ```bash
   pm2 status
   pm2 logs legal-bot
   ```

---

## 🖥️ VPS Deployment (DigitalOcean/Linode)

### Cost: $4-5/month

### DigitalOcean Steps:

1. **Create Account**: https://www.digitalocean.com
   - Get $200 free credit for 60 days with referral

2. **Create Droplet**:
   - Image: Ubuntu 22.04 LTS
   - Plan: Basic ($4/month)
   - Region: Closest to India (Bangalore)

3. **SSH to Server**:
   ```bash
   ssh root@your-droplet-ip
   ```

4. **Install Bot**:
   ```bash
   # Update system
   apt update && apt upgrade -y

   # Install Python
   apt install python3-pip git -y

   # Clone and install
   git clone <your-repo-url>
   cd kakinada-legal-bot
   pip3 install -r requirements.txt

   # Install screen (to keep bot running)
   apt install screen -y

   # Start bot in screen session
   screen -S bot
   python3 bot.py
   # Press Ctrl+A then D to detach

   # To reattach later
   screen -r bot
   ```

5. **Auto-restart on Reboot**:
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/legal-bot.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=Kakinada Legal Assistant Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/kakinada-legal-bot
   ExecStart=/usr/bin/python3 /root/kakinada-legal-bot/bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable legal-bot
   sudo systemctl start legal-bot
   sudo systemctl status legal-bot
   ```

---

## 🔒 Security Best Practices

### 1. Move API Keys to Environment Variables

Update `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
```

Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk
GEMINI_API_KEY=AIzaSyC1DRSmrGVvxMzARHhsLWTqiwpSVPLEOmI
GOOGLE_MAPS_API_KEY=AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ
```

Add to `.gitignore`:
```
.env
*.pyc
__pycache__/
```

### 2. Update `.gitignore`
```gitignore
.env
*.pyc
__pycache__/
*.pdf
*.log
venv/
.DS_Store
```

---

## 📊 Monitoring & Maintenance

### Health Check Script

Create `health_check.py`:
```python
import requests
import time

BOT_TOKEN = "8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk"

def check_bot_status():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ Bot is running!")
            return True
        else:
            print("❌ Bot is down!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    while True:
        check_bot_status()
        time.sleep(300)  # Check every 5 minutes
```

### Logging

Add to your bot:
```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🎯 Recommended Deployment Path

### For Beginners (FREE):
```
1. Push code to GitHub
2. Deploy to Render (5 minutes)
3. Monitor via Render dashboard
4. Done! ✅
```

### For Production (Paid):
```
1. Buy DigitalOcean Droplet ($4/month)
2. Setup with systemd service
3. Configure auto-restart
4. Setup monitoring
5. Done! ✅
```

---

## 🆘 Troubleshooting

### Bot Not Starting?

1. **Check Logs**:
   ```bash
   # Render: View in dashboard
   # VPS: pm2 logs OR systemctl status legal-bot
   ```

2. **Test Locally**:
   ```bash
   python bot.py
   ```

3. **Check Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify API Keys**:
   - Test Telegram token
   - Test Gemini API key
   - Test Google Maps key

### Bot Crashing?

1. **Enable Auto-restart** (covered above)
2. **Check Memory Usage** - Upgrade plan if needed
3. **Review Error Logs**
4. **Test with smaller features first**

---

## 📞 Support

If you face issues:
1. Check logs first
2. Test API keys
3. Verify internet connection on server
4. Check firewall settings
5. Review platform-specific docs

---

## ✅ Quick Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] requirements.txt updated
- [ ] API keys secured (use .env)
- [ ] .gitignore configured
- [ ] Tested locally
- [ ] Selected deployment platform
- [ ] Monitoring setup
- [ ] Auto-restart configured

---

## 🎉 After Deployment

Your bot is now running 24/7! 🚀

**Test it**:
1. Open Telegram
2. Send `/start` to your bot
3. Try all commands
4. Monitor logs for errors

**Maintain it**:
- Check logs weekly
- Update dependencies monthly
- Monitor uptime
- Backup your code

---

**Made with ❤️ for Kakinada Legal Assistant Bot**

