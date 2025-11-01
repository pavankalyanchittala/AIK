# 🤖 Smart Complaint Type Detection

## Overview

The bot now uses **AI-powered intelligent complaint type detection**. Users no longer need to know the exact legal terminology - they can simply describe what happened in their own words, and the bot will automatically identify the complaint type!

---

## 🎯 How It Works

### Old Flow ❌
```
Bot: What type of complaint do you want to file?
User: Uh... I don't know... someone took my phone?
❌ User needs to know legal terms
```

### New Smart Flow ✅
```
Bot: Describe what happened in your own words
User: Someone came and took my mobile phone yesterday
Bot: 🤔 Analyzing...
Bot: ✅ I understand this is about: **Theft**
     Is this correct?
     • Type 'yes' to confirm
     • Type your own (e.g., 'Fraud')  
     • Type 'skip' if not sure
User: yes ✓
```

---

## 📋 Complaint Filing Process

### Step-by-Step Flow

1. **Personal Details** 📝
   - Name
   - Father's/Husband's name
   - Age
   - Phone number
   - Email (optional)
   - Address

2. **Incident Description** 💬 ⭐ **NEW**
   - User describes in their own words
   - No legal jargon needed
   - Natural language input

3. **AI Analysis** 🤖 ⭐ **NEW**
   - Bot analyzes the description
   - Identifies complaint type
   - Uses Google Search for context

4. **Confirmation** ✅ ⭐ **NEW**
   - Bot shows detected type
   - User can:
     - Confirm with "yes"
     - Type their own if wrong
     - Skip if unsure

5. **Additional Details** 📅
   - When did it happen?
   - Where did it happen?
   - Any additional details?

6. **PDF Generation** 📄
   - Location-aware police stations
   - Applicable laws
   - Download complaint PDF

---

## 🧠 AI Detection Examples

### Example 1: Theft Detection
```
User Input: "Someone stole my mobile phone from my bag"
AI Detects: Theft
Applicable Laws: IPC Section 379
```

### Example 2: Fraud Detection
```
User Input: "A person promised to double my money but disappeared with ₹50,000"
AI Detects: Fraud / Cheating
Applicable Laws: IPC Section 420
```

### Example 3: Harassment Detection
```
User Input: "My neighbor keeps threatening me and my family daily"
AI Detects: Harassment / Criminal Intimidation
Applicable Laws: IPC Section 506
```

### Example 4: Cyber Crime Detection
```
User Input: "Someone hacked my Instagram account and is posting fake messages"
AI Detects: Cyber Crime
Applicable Laws: IT Act Section 66
```

### Example 5: Domestic Violence Detection
```
User Input: "My husband beats me every day and doesn't let me go out"
AI Detects: Domestic Violence
Applicable Laws: Protection of Women from Domestic Violence Act
```

---

## 💡 User-Friendly Features

### 1. Natural Language Input
- Users can type in **any language style**
- No need to know legal terms
- Conversational tone accepted

### 2. Multiple Response Options
When bot suggests a type, users can:

| Response | Action |
|----------|--------|
| "yes", "y", "ok", "correct" | Confirms AI suggestion |
| "Theft", "Fraud", etc. | Uses user's custom type |
| "skip" | Sets as "General Complaint" |

### 3. Error Handling
If AI can't detect:
- Falls back to manual input
- Shows common examples
- User can still skip

---

## 🔧 Technical Implementation

### In `bot.py`

#### New Function: `complaint_initial_description`

```python
async def complaint_initial_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get initial incident description and auto-detect complaint type"""
    description = update.message.text
    context.user_data['complaint']['initial_description'] = description
    
    # Show analyzing message
    await update.message.reply_text("🤔 Analyzing your complaint...")
    
    try:
        # Use AI to detect complaint type
        analysis_prompt = f"""Based on this incident description, 
        identify the most appropriate complaint type.
        
        Description: "{description}"
        
        Choose from: Theft, Robbery, Fraud, Cheating, Harassment, 
        Cyber Crime, Domestic Violence, Property Dispute, Assault, 
        Kidnapping, Missing Person, Traffic Violation, Forgery
        """
        
        user_id = update.message.from_user.id
        ai_response = legal_bot.send_message(user_id, analysis_prompt)
        
        # Extract and clean complaint type
        complaint_type = extract_type(ai_response)
        
        # Ask for confirmation
        await update.message.reply_text(
            f"✅ I understand this is about: **{complaint_type}**\n\n"
            f"Is this correct?\n"
            f"• Type 'yes' to confirm\n"
            f"• Type the correct type\n"
            f"• Type 'skip' if unsure"
        )
        
    except Exception as e:
        # Fallback to manual input
        await update.message.reply_text(
            "What type of complaint is this?\n"
            "Examples: Theft, Fraud, Harassment\n"
            "Or type 'skip' if not sure"
        )
```

#### Updated Function: `complaint_type`

```python
async def complaint_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle complaint type confirmation"""
    user_input = update.message.text.strip()
    
    if user_input.lower() in ['yes', 'correct', 'ok', 'y']:
        # User confirmed AI suggestion
        complaint_type = context.user_data['complaint'].get('suggested_type')
    elif user_input.lower() == 'skip':
        complaint_type = "General Complaint"
    else:
        # User typed their own
        complaint_type = user_input
    
    context.user_data['complaint']['complaint_type'] = complaint_type
    # Continue to next step...
```

---

## 📊 Benefits

### For Users
✅ **No Legal Knowledge Needed** - Describe in plain language  
✅ **Faster Process** - Less confusion about terminology  
✅ **More Accurate** - AI suggests the right type  
✅ **Flexible** - Can still customize if needed  

### For Legal Processing
✅ **Better Categorization** - Consistent complaint types  
✅ **Proper Laws Applied** - Accurate IPC section mapping  
✅ **Location Intelligence** - Right police station suggested  
✅ **Evidence Trail** - Full description captured  

---

## 🎨 User Experience Flow

```
┌─────────────────────────────────────┐
│ User describes incident naturally   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ AI analyzes with Google Search      │
│ - Identifies complaint type          │
│ - Checks legal definitions           │
│ - Matches with IPC sections          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Bot presents suggestion              │
│ "This seems like: THEFT"             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ User confirms/modifies/skips         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Rest of complaint process            │
│ - Date/time                          │
│ - Location                           │
│ - Additional details                 │
│ - PDF generation                     │
└─────────────────────────────────────┘
```

---

## 🚀 Future Enhancements

1. **Multi-language Support**
   - Telugu, Hindi, English
   - Auto-translate descriptions

2. **Voice Input**
   - Voice messages accepted
   - Speech-to-text conversion
   - For illiterate users

3. **Image Analysis**
   - Upload evidence photos
   - OCR for documents
   - AI analyzes images

4. **Severity Detection**
   - Urgent vs non-urgent
   - Auto-prioritization
   - Quick response for emergencies

5. **Similar Cases**
   - Show similar complaints
   - Previous outcomes
   - Legal precedents

---

## 💬 Sample Conversations

### Conversation 1: Theft
```
Bot: Describe what happened
User: My bag was stolen from railway station
Bot: 🤔 Analyzing...
Bot: ✅ This is about: **Theft**
     Confirm? (yes/no/skip)
User: yes
Bot: When did this happen?
User: yesterday evening
Bot: Where exactly?
User: Kakinada railway station platform 1
Bot: Any additional details?
User: CCTV cameras were there, I have screenshots
Bot: ✅ Complaint generated!
     📍 Nearest police station: Kakinada Town Police
     📄 PDF ready for download
```

### Conversation 2: Online Fraud
```
Bot: Describe what happened
User: I paid money on OLX but seller blocked me
Bot: 🤔 Analyzing...
Bot: ✅ This is about: **Online Fraud / Cyber Crime**
     Confirm? (yes/no/skip)
User: yes
Bot: When did this happen?
User: 2 days ago, I paid ₹15000
Bot: Where was the seller located?
User: Somewhere in Delhi, don't know exact address
Bot: Any additional details?
User: I have payment screenshots and chat history
Bot: ✅ Complaint generated!
     ⚠️ For cyber crime, also file at: cybercrime.gov.in
     📍 Local police: Kakinada Cyber Cell
     📄 PDF ready for download
```

---

## 📞 Support

If AI detection fails:
- User can manually type complaint type
- User can skip and use "General Complaint"
- Bot still generates proper PDF
- Police will categorize correctly

---

**Remember**: The AI suggestion is to help users, not restrict them. Users always have the final say in what their complaint type should be!

