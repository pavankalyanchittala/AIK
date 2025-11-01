# 🔍 Google Search Integration - Usage Guide

## Overview

The Kakinada Legal Assistant Bot now uses **Google Search** powered by the new `google-genai` SDK to provide **real-time, up-to-date** information.

---

## 🎯 When Google Search is Used

The AI automatically searches the internet for these types of queries:

### 1. **Laws & Legal Information** 📚
- Latest IPC sections and amendments
- New acts and legal provisions
- Recent court judgments and precedents
- Changes in criminal/civil law

**Example Questions:**
- "What is Section 420 IPC?"
- "Latest amendments in IPC 2024"
- "What are consumer rights in India?"
- "Recent Supreme Court judgments on property disputes"

### 2. **Government Schemes** 🏛️
- Current active schemes (Central & State)
- Eligibility criteria and requirements
- Application processes and deadlines
- Scheme benefits and documentation

**Example Questions:**
- "What is PM Kisan Yojana?"
- "Andhra Pradesh government schemes 2024"
- "How to apply for Ayushman Bharat?"
- "Housing schemes in Kakinada"

### 3. **Police Station Locations** 🚔
- Police stations near user's city/district
- Contact numbers and addresses
- Emergency helplines by location
- Jurisdiction information

**Example Questions:**
- "Police stations in Vijayawada"
- "Kakinada police station contact"
- "Nearest police station to me"
- "Emergency numbers in Andhra Pradesh"

### 4. **Complaint/FIR Procedures** 📝
- Latest filing procedures
- Required documents and evidence
- Online vs offline filing methods
- What to expect after filing

**Example Questions:**
- "How to file an FIR online?"
- "What documents needed for theft complaint?"
- "Procedure to file cyber crime complaint"
- "Can I file FIR online in Andhra Pradesh?"

### 5. **Recent Legal Changes** ⚖️
- Law reforms in past 2 years
- Policy updates
- New regulations
- Court directive changes

**Example Questions:**
- "New laws in India 2024"
- "Recent changes in consumer protection act"
- "Latest updates on domestic violence act"
- "What changed in motor vehicles act?"

---

## 🤖 How It Works

### Technical Implementation

```python
# The bot uses Google GenAI SDK with Google Search tool
from google import genai
from google.genai import types

# Configure Google Search
tools = [
    types.Tool(googleSearch=types.GoogleSearch())
]

# Send queries with search enabled
response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=user_message,
    config=config_with_google_search
)
```

### AI Search Strategy

The AI is instructed to use specific search patterns:

| Query Type | Search Pattern |
|------------|----------------|
| Laws | "latest [law name] amendments 2024 India" |
| Schemes | "[scheme name] eligibility 2024 Andhra Pradesh" |
| Police | "police stations in [city] Andhra Pradesh contact" |
| Procedures | "how to file [complaint type] India 2024" |

---

## ✅ Benefits

### 1. **Always Up-to-Date** 📅
- Gets latest information from the web
- No outdated law information
- Current scheme details

### 2. **Location-Aware** 📍
- Finds police stations in user's actual city
- Not limited to Kakinada only
- State-specific scheme information

### 3. **Accurate Legal Info** ⚖️
- Verifies IPC sections before answering
- Checks for recent amendments
- Provides source-backed answers

### 4. **Real Government Schemes** 🎯
- Only active schemes mentioned
- Current eligibility criteria
- Live application procedures

---

## 💡 Pro Tips

### For Users

1. **Be Specific**: Instead of "laws", ask "Section 420 IPC"
2. **Mention Location**: "Police stations in Vijayawada" vs just "police"
3. **Include Year**: "Government schemes 2024" gets latest results
4. **Ask About Recent Changes**: "Latest updates in..." triggers search

### For Developers

1. **System Prompt**: The AI is instructed to search for specific topics
2. **Context Added**: User queries include location context
3. **Response Format**: AI cites sources when using search results
4. **Fallback**: If search fails, provides general knowledge

---

## 🔧 Configuration

### In `config.py`:

```python
LEGAL_ASSISTANT_PROMPT = """
CRITICAL - ALWAYS USE GOOGLE SEARCH FOR:
1. Laws & Legal Information
2. Government Schemes
3. Police Stations
4. Complaint/FIR Procedures
5. Recent Legal Changes

SEARCH STRATEGY:
- For laws: Search "latest [law name] amendments 2024 India"
- For schemes: Search "[scheme name] eligibility 2024 Andhra Pradesh"
- For police: Search "police stations in [city] Andhra Pradesh contact"
- For procedures: Search "how to file [complaint type] India 2024"
"""
```

### In `bot.py`:

```python
# Google Search tool enabled by default
self.tools = [
    types.Tool(googleSearch=types.GoogleSearch())
]

# Used in all AI responses
self.generation_config = types.GenerateContentConfig(
    temperature=0.7,
    system_instruction=config.LEGAL_ASSISTANT_PROMPT,
    tools=self.tools  # Google Search enabled
)
```

---

## 📊 Example Conversations

### Example 1: Law Query
```
User: What is Section 420 IPC?
Bot: 🔍 [Searches: "Section 420 IPC latest amendments 2024"]

Section 420 of the Indian Penal Code deals with cheating 
and dishonestly inducing delivery of property. It provides 
for imprisonment up to 7 years and fine.

Recent Update: [Search result shows if any amendments]
Source: [Cites source if available]
```

### Example 2: Scheme Query
```
User: PM Kisan scheme eligibility
Bot: 🔍 [Searches: "PM Kisan eligibility 2024 India"]

PM-KISAN Eligibility (2024):
✅ Small and marginal farmers
✅ Landholding up to 2 hectares
✅ All farmer families eligible

Amount: ₹6000/year in 3 installments
Apply: [Latest application process from search]
```

### Example 3: Location-Aware
```
User: I'm in Vijayawada, mobile stolen
Bot: 🔍 [Searches: "police stations in Vijayawada contact"]

⚠️ Detected location: Vijayawada

Nearest Police Stations:
📍 Governorpet Police Station
📞 0866-2574671

📍 Benz Circle Police Station
📞 [Number from search]

File complaint immediately at nearest station!
```

---

## 🚀 Future Enhancements

1. **Image Search**: Analyze legal documents in images
2. **Voice Search**: Audio queries for illiterate users
3. **Multi-language**: Search in Telugu + English
4. **Case Law Search**: Specific court judgment searches
5. **Scheme Alerts**: Notify about new schemes

---

## 📞 Support

For issues or improvements:
- Check logs for search errors
- Verify GEMINI_API_KEY is valid
- Ensure internet connection is stable
- Check if Google Search quota is available

---

**Note**: Google Search is integrated at the model level, so every relevant query automatically triggers a search without user intervention. The AI decides when to search based on the query type.

