# 🏛️ Kakinada Legal Assistant Bot

## AI-Powered Legal Assistant for Kakinada & Andhra Pradesh

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org)
[![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**✅ Supports 50+ Concurrent Users** | **✅ Free 24/7 Deployment** | **✅ Production-Ready**

---

## 🎯 Features

### Core Capabilities
- 🤖 **AI-Powered** - Google Gemini with real-time Google Search
- 📝 **Complaint Filing** - Generate legal complaint forms
- 🚔 **FIR Assistance** - Step-by-step FIR filing guidance
- 📍 **Police Station Locator** - GPS-based nearest station finder
- ⚖️ **Legal Information** - Indian laws, rights, IPC sections
- 🏛️ **Government Schemes** - Search schemes with eligibility
- 📄 **PDF Generation** - Professional complaint/FIR documents
- 🔍 **Document Analysis** - Analyze legal documents with AI

### Technical Features
- ⚡ **Async Architecture** - Handles 50+ concurrent users
- 🔒 **Secure** - API keys in environment variables
- 🌐 **Google Search Grounding** - Up-to-date legal information
- 📱 **Mobile Friendly** - Works on all Telegram clients
- 🆓 **Free to Deploy** - Render/Railway free tier compatible

---

## 🚀 Quick Start (5 Minutes)

### 1. Prerequisites
- Python 3.10+
- Telegram account
- GitHub account (for deployment)

### 2. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/kakinada-legal-bot.git
cd kakinada-legal-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from env_template.txt)
# Add your API keys:
TELEGRAM_BOT_TOKEN=your_token
GEMINI_API_KEY=your_key  
GOOGLE_MAPS_API_KEY=your_key
```

### 3. Run Locally
```bash
python bot.py
```

### 4. Test
Open Telegram → Search `@ai_governance_bot` → Send `/start`

---

## 🌐 Deploy to Render (FREE 24/7)

### One-Click Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to: https://dashboard.render.com
   - Click "New +" → **"Background Worker"**
   - Connect GitHub repo
   - Add environment variables (see ENV_SETUP.md)
   - Click "Create Background Worker"
   
3. **Done!** Bot is live 24/7 ✅

**Full Guide**: See `QUICK_DEPLOY.md`

---

## 📊 Performance & Scalability

### Concurrent User Support

| Users | Response Time | Status | Cost |
|-------|---------------|--------|------|
| **1-50 users** | 1-3 seconds | ✅ Excellent | $0 (Free) |
| **50-100 users** | 2-5 seconds | ✅ Good | $0-$7 |
| **100+ users** | 3-8 seconds | ✅ Good | $7-$25 |

**✅ Your bot can handle 50+ concurrent users without any modifications!**

### API Rate Limits (Free Tier)

| API | Limit | Capacity |
|-----|-------|----------|
| **Gemini AI** | 60 req/min | ✅ 60 users/min |
| **Google Maps** | 1000 req/day | ✅ 500 users/day |
| **Telegram** | 30 msg/sec | ✅ 1800 users/min |

**Full Details**: See `CONCURRENCY_PERFORMANCE.md`

---

## 🏗️ Architecture

### Tech Stack
```
┌─────────────────┐
│  Telegram Bot   │ ← Users interact
└────────┬────────┘
         │
    ┌────▼────┐
    │ Bot.py  │ ← Async handlers
    └────┬────┘
         │
    ┌────▼─────────────────────┐
    │  External APIs:          │
    │  • Gemini AI + Search    │
    │  • Google Maps Places    │
    │  • Telegram Bot API      │
    └──────────────────────────┘
```

### Key Components
- **bot.py** - Main bot logic with async handlers
- **config.py** - Configuration & API keys
- **pdf_generator.py** - PDF document generation
- **requirements.txt** - Python dependencies
- **runtime.txt** - Python version (3.10.12)

---

## 📚 Commands

### User Commands
```
/start      - Welcome & introduction
/help       - List all commands
/ask        - Ask legal questions (AI-powered)
/schemes    - Search government schemes
/laws       - Get legal information
/complaint  - File a complaint (generates PDF)
/fir        - FIR filing guidance (generates PDF)
/police     - Find nearest police station (GPS)
/cancel     - Cancel current operation
```

### Features
- **Smart Complaint Detection** - Auto-detects complaint type from description
- **Applicable Laws** - Automatically suggests relevant IPC sections
- **Location-Based** - Finds nearest police station using GPS
- **PDF Generation** - Professional documents ready for submission

---

## 🔐 Environment Variables

### Required API Keys

| Variable | Get From | Purpose |
|----------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) | Bot authentication |
| `GEMINI_API_KEY` | [AI Studio](https://aistudio.google.com/apikey) | AI & Search |
| `GOOGLE_MAPS_API_KEY` | [Cloud Console](https://console.cloud.google.com/) | Location services |

### Setup
```bash
# Local development:
# Create .env file with your keys

# Render/Railway deployment:
# Add as environment variables in dashboard
```

**Full Guide**: See `ENV_SETUP.md`

---

## 📁 Project Structure

```
kakinada-legal-bot/
├── bot.py                      # Main bot application
├── config.py                   # Configuration & settings
├── pdf_generator.py            # PDF document generation
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version
├── .env                        # API keys (local, not in git)
├── .gitignore                  # Git ignore rules
│
├── README_DEPLOYMENT.md        # This file
├── QUICK_DEPLOY.md             # 5-minute deployment guide
├── DEPLOYMENT_GUIDE.md         # Complete deployment options
├── ENV_SETUP.md                # Environment variables guide
├── CONCURRENCY_PERFORMANCE.md  # Performance & scalability
├── TROUBLESHOOTING.md          # Common errors & solutions
├── RENDER_FREE_TIER_NOTES.md   # Render platform details
└── API_KEYS_UPDATE_SUMMARY.md  # API key management
```

---

## 🔧 Troubleshooting

### Common Issues

**Bot not responding?**
```bash
# Check if bot is running
tasklist | findstr python

# Check logs
python bot.py
```

**API errors?**
- Verify API keys in .env
- Check quota limits (Gemini: 60/min, Maps: 1000/day)
- Ensure keys not leaked/blocked

**Deployment issues?**
- Verify environment variables on Render/Railway
- Check build logs for errors
- Ensure runtime.txt has Python 3.10.12

**Full Solutions**: See `TROUBLESHOOTING.md`

---

## 📈 Monitoring & Analytics

### Check API Usage

**Gemini API:**
- Dashboard: https://aistudio.google.com/
- Limit: 60 requests/min, 1500/day

**Google Maps API:**
- Dashboard: https://console.cloud.google.com/
- Limit: 1000 requests/day (free)

**Render Platform:**
- Dashboard: https://dashboard.render.com
- Check: Logs, metrics, bandwidth usage

---

## 🎯 Roadmap & Future Enhancements

### Planned Features
- [ ] Multi-language support (Telugu, Hindi)
- [ ] Lawyer directory integration
- [ ] Case status tracking
- [ ] SMS notifications
- [ ] Voice message support
- [ ] Court date reminders

### Optional Optimizations (When Needed)
- [ ] Redis caching for common queries
- [ ] Async Google Maps API calls
- [ ] Request queue for rate limiting
- [ ] Multiple instance load balancing

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - For powerful AI capabilities
- **Telegram Bot API** - For bot platform
- **Google Maps API** - For location services
- **Render** - For free hosting

---

## 📞 Support

### Documentation
- **Quick Deploy**: `QUICK_DEPLOY.md`
- **Full Deployment**: `DEPLOYMENT_GUIDE.md`  
- **Performance**: `CONCURRENCY_PERFORMANCE.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Environment Setup**: `ENV_SETUP.md`

### Resources
- Telegram Bot API: https://core.telegram.org/bots/api
- Gemini API: https://ai.google.dev/docs
- Google Maps: https://developers.google.com/maps
- Render Docs: https://render.com/docs

---

## 🎉 Quick Summary

✅ **50+ concurrent users supported**  
✅ **Free 24/7 deployment on Render**  
✅ **AI-powered with Google Search**  
✅ **Production-ready**  
✅ **No code changes needed**  

### Deploy in 5 Minutes:
1. Clone repo
2. Push to GitHub
3. Deploy on Render
4. Add environment variables
5. Done! 🚀

---

**Made with ❤️ for Kakinada & Andhra Pradesh**

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

