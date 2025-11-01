# 📋 Render Free Tier - Important Notes

Based on official documentation: https://render.com/docs/free

## ✅ What You Get FREE

### Monthly Allowances (Per Workspace)
- **750 Free instance hours** - Perfect for 24/7 bot operation
  - Calculation: 31 days × 24 hours = 744 hours (just enough!)
- **100 GB outbound bandwidth**
- **Build pipeline minutes** (varies by plan)

### Features Included
- ✅ Auto-deploy from GitHub/GitLab
- ✅ HTTPS/SSL certificates
- ✅ Custom domains
- ✅ Log streaming (real-time)
- ✅ Rollbacks (last 2 deploys)
- ✅ Service previews
- ✅ No credit card required

---

## ⚠️ Critical Limitations

### 1. Background Workers vs Web Services

**For Telegram Bots - Use BACKGROUND WORKER!**

| Feature | Background Worker | Web Service |
|---------|------------------|-------------|
| **Runs 24/7** | ✅ YES | ❌ Spins down after 15 min idle |
| **Always responsive** | ✅ YES | ❌ 30-60s delay after idle |
| **Perfect for bots** | ✅ YES | ❌ NO |
| **Consumes hours** | While running | While running (not when spun down) |

**Important**: 
- Web Services spin down after 15 minutes of no HTTP traffic
- Telegram bots don't receive HTTP requests (they poll for updates)
- Therefore, Web Services are **NOT suitable** for Telegram bots
- Always use **Background Worker** for Telegram bots

Reference: [Render Free Tier - Spinning down on idle](https://render.com/docs/free#spinning-down-on-idle)

---

### 2. Monthly Hour Limits

```
750 Free instance hours per workspace per month
```

**What This Means:**
- 1 Background Worker running 24/7 = 744 hours/month ✅ (fits perfectly!)
- 2 Background Workers running 24/7 = 1488 hours/month ❌ (exceeds limit)

**If You Exceed 750 Hours:**
- Render **suspends all Free services** until next month
- Hours reset on the 1st of each month
- No rollover of unused hours

**Tracking Usage:**
- Dashboard → Billing → "Monthly Included Usage"
- Render sends email warnings at 80% and 100%

Reference: [Render Free Tier - Monthly usage limits](https://render.com/docs/free#monthly-usage-limits)

---

### 3. Bandwidth Limits

**Outbound Bandwidth:**
- Free tier includes a certain amount monthly
- If exceeded:
  - With payment method: Billed for extra bandwidth
  - Without payment method: Services suspended

**For This Bot:**
- Telegram messages: ~1-5 KB each
- PDFs: ~50-200 KB each
- Google Maps API calls: ~5-10 KB each
- Estimated: ~100-500 users/month = well within limits

Reference: [Render Free Tier - Bandwidth](https://render.com/docs/free#bandwidth-and-build-pipeline)

---

### 4. Service Restarts

**Render May Restart Your Service:**
- At any time without notice
- For platform maintenance
- To manage resources

**Impact on Your Bot:**
- ~10-30 seconds downtime during restart
- Bot automatically reconnects to Telegram
- No data loss (conversation states may reset)
- Happens rarely (usually 1-2 times per month)

**Mitigation:**
- Use Background Worker (auto-restarts)
- Implement proper error handling (already done)
- Don't store critical data in memory

---

### 5. No Persistent Disk

**Free instances don't support persistent disks:**
- Files written to disk are **temporary**
- Lost on every restart
- Don't use for permanent storage

**For This Bot:**
- ✅ PDFs generated on-demand and sent immediately
- ✅ No permanent file storage needed
- ✅ All config in code/environment variables
- ✅ No impact on functionality

Reference: [Render Free Tier - Other limitations](https://render.com/docs/free#other-limitations)

---

### 6. Network Restrictions

**Free services cannot:**
- ❌ Send outbound traffic on ports 25, 465, 587 (SMTP)
- ❌ Receive private network traffic
- ❌ Listen on reserved ports 18012, 18013, 19099

**For This Bot:**
- ✅ Uses Telegram API (port 443) - allowed
- ✅ Uses Gemini API (port 443) - allowed
- ✅ Uses Google Maps API (port 443) - allowed
- ✅ No email sending needed
- ✅ No impact on functionality

Reference: [Render Free Tier - Other limitations](https://render.com/docs/free#other-limitations)

---

## 📊 Free Postgres Limitations

**If you add a Free Postgres database (not needed for this bot):**

⚠️ **30-Day Expiration!**
- Free Postgres databases expire after 30 days
- 14-day grace period to upgrade or it's deleted
- 1 GB storage limit
- Only 1 free database per workspace
- **No backups**

**For This Bot:**
- ✅ No database needed
- ✅ All data from APIs in real-time
- ✅ Conversation state managed by python-telegram-bot
- ✅ No impact

Reference: [Render Free Tier - Free Postgres](https://render.com/docs/free#free-postgres)

---

## 💰 When to Upgrade?

### Stay on FREE if:
- ✅ Bot has < 500 active users/month
- ✅ Usage < 750 hours/month (1 bot 24/7)
- ✅ Bandwidth < 100 GB/month
- ✅ Occasional restarts acceptable (1-2/month)
- ✅ No SLA requirements

### Upgrade to Starter ($7/month) if:
- ❌ Need guaranteed uptime
- ❌ Bot has > 500 active users
- ❌ Need multiple services
- ❌ Need persistent disk storage
- ❌ Need more resources (RAM/CPU)

---

## 🎯 Perfect Use Cases for Render Free Tier

### ✅ Great For:
1. **Testing & Development** - Perfect for testing your bot
2. **Personal Projects** - Hobby bots with light usage
3. **MVPs & Demos** - Show your bot to potential users
4. **Learning** - Learn deployment without costs
5. **Low-Traffic Bots** - < 500 users/month

### ❌ Not Suitable For:
1. **Production Apps** - High uptime requirements
2. **High Traffic** - > 1000 users/day
3. **Critical Services** - Can't tolerate restarts
4. **Data Storage** - Need persistent files/database
5. **Email Services** - SMTP ports blocked

---

## 📈 Monitoring Your Usage

### In Render Dashboard:

1. **Go to Billing Page**
2. **View "Monthly Included Usage" Section**
3. **Track These Metrics:**
   - Free instance hours used / 750
   - Outbound bandwidth used / limit
   - Build minutes used / limit

### Email Notifications:
- **80% usage**: Warning email
- **100% usage**: Alert email (service may suspend)

### Best Practices:
- Check usage weekly
- Set calendar reminder for 20th of each month
- Plan upgrade before hitting limits

---

## 🚀 Deployment Strategy

### For This Bot (Kakinada Legal Assistant):

```
Service Type: Background Worker ✅
Instance Type: Free ✅
Region: Singapore (closest to India) ✅
Expected Hours: 744/month (24/7) ✅
Expected Bandwidth: < 10 GB/month ✅
Database Needed: No ✅
Persistent Disk: No ✅

Verdict: PERFECT FIT for Render Free Tier! ✅
```

---

## 📞 Support & Resources

- **Render Docs**: https://render.com/docs
- **Free Tier Limits**: https://render.com/docs/free
- **Status Page**: https://status.render.com
- **Community Forum**: https://community.render.com
- **Support Email**: support@render.com (paid plans only)

---

## ✅ Final Checklist

Before deploying:
- [ ] Choose "Background Worker" (NOT Web Service)
- [ ] Select "Free" instance type
- [ ] Choose Singapore region
- [ ] Verify `requirements.txt` is complete
- [ ] Confirm `runtime.txt` has `python-3.10.12`
- [ ] Test bot locally first
- [ ] Push code to GitHub
- [ ] Connect repo to Render
- [ ] Monitor first 24 hours of operation
- [ ] Check usage after 1 week

After deploying:
- [ ] Test all bot commands
- [ ] Verify PDF generation works
- [ ] Test location sharing
- [ ] Monitor logs for errors
- [ ] Set calendar reminder to check usage monthly

---

**Last Updated**: November 2025  
**Documentation Version**: Render Free Tier (2025)  
**Bot Compatibility**: ✅ Fully Compatible

---

**Made with ❤️ for Kakinada Legal Assistant Bot**

