# 🏛️ Kakinada Legal Assistant Bot

A powerful Telegram bot that serves as your AI-powered legal assistant for Kakinada, Andhra Pradesh, and India. Built with Google's Gemini AI and powered by Google Search for real-time legal information.

## ✨ Features

- 🤖 **AI-Powered Legal Assistant** - Powered by Gemini Flash-Lite model with Google Search integration
- ⚖️ **Legal Information** - Get information about Indian laws, rights, and legal procedures
- 🏛️ **Government Schemes** - Learn about government schemes and policies
- 📝 **Smart Complaint Filing** - AI analyzes your complaint and suggests applicable laws
- 🚔 **Intelligent FIR Filing** - Automatic crime type detection and legal section recommendations
- 📄 **PDF Generation** - Auto-generate complaint and FIR documents in PDF format
- 📍 **Location-Aware** - Detects your city and provides appropriate police contacts
- 🗺️ **Multi-City Support** - Works for Kakinada, Vijayawada, Visakhapatnam, Tirupati, Guntur
- 🔍 **Document Analysis** - Upload and analyze legal documents and images
- 📸 **Image Support** - Send images for AI analysis and guidance
- 🧠 **Context Understanding** - Understands "mobile theft" even if you just say "mobile"
- ⚡ **Real-time Information** - Get up-to-date legal information with Google Search grounding

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram account
- Google Gemini API key (already configured)
- Telegram Bot Token (already configured)

### Installation

1. **Clone or download this repository**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Run the bot:**
```bash
python bot.py
```

4. **Open Telegram and search for:** `@ai_governance_bot`

5. **Start chatting with the bot!**

## 📱 How to Use

### Starting the Bot

1. Open Telegram and search for `@ai_governance_bot`
2. Click "Start" or send `/start`
3. Choose from the menu options or ask any legal question

### Available Commands

- `/start` - Start the bot and see main menu
- `/help` - Show help and usage information
- `/complaint` - Start interactive complaint filing
- `/fir` - Start interactive FIR filing
- `/police` - Get nearby police stations
- `/schemes` - Learn about government schemes
- `/laws` - Get legal information
- `/cancel` - Cancel current operation

### Filing a Complaint

1. Send `/complaint` command
2. Answer the interactive questions:
   - Personal details (name, age, contact)
   - Complaint type
   - Incident details
   - Description
3. Receive:
   - Applicable law sections
   - Nearest police stations
   - PDF complaint form ready to submit

### Filing an FIR

1. Send `/fir` command
2. Provide detailed information:
   - Personal details
   - Crime details
   - Accused information (if known)
   - Incident description
3. Receive:
   - FIR draft in PDF format
   - Applicable IPC sections
   - Police station recommendations
   - Next steps guidance

### Ask Legal Questions

Simply type your question in natural language:

- "What are my rights as a tenant?"
- "How do I file a consumer complaint?"
- "Tell me about the Right to Information Act"
- "What is Section 498A IPC?"
- "How can I apply for PM Kisan Yojana?"

### Document Analysis

- Send any legal document or image
- The bot will analyze it using AI
- Get relevant information and guidance

## 🏢 Kakinada Police Stations

The bot has information about these police stations:

1. **Kakinada Town Police Station**
   - Address: Main Road, Kakinada-533001
   - Phone: 0884-2365555

2. **Kakinada Rural Police Station**
   - Address: Kakinada Rural, East Godavari District
   - Phone: 0884-2367777

3. **Kakinada One Town Police Station**
   - Address: Suryanarayana Puram, Kakinada-533003
   - Phone: 0884-2369999

4. **Kakinada Two Town Police Station**
   - Address: Sarpavaram Junction, Kakinada-533005
   - Phone: 0884-2371111

5. **Women Police Station, Kakinada**
   - Address: Beside District Court, Kakinada-533001
   - Phone: 0884-2373333

6. **Cyber Crime Police Station, Kakinada**
   - Address: SP Office Complex, Kakinada
   - Phone: 0884-2375555

## 🚨 Emergency Numbers

- **Police Emergency:** 100
- **National Emergency:** 112
- **Women Helpline:** 181
- **Child Helpline:** 1098

## 📋 Common IPC Sections

The bot can provide information about:

- **IPC 378-379** - Theft
- **IPC 323, 325** - Assault and hurt
- **IPC 354, 509** - Harassment and outraging modesty
- **IPC 420** - Fraud and cheating
- **IPC 498A** - Domestic violence
- **IT Act Sections** - Cyber crimes
- **IPC 441, 447** - Property disputes
- **IPC 499-500** - Defamation
- And many more...

## 🛠️ Technical Details

### Technologies Used

- **Python 3.8+**
- **python-telegram-bot 20.7** - Telegram Bot API wrapper
- **google-generativeai** - Google Gemini AI integration
- **ReportLab** - PDF generation
- **Pillow** - Image processing

### Features Implementation

- ✅ Conversational AI with context awareness
- ✅ Multi-turn conversations for complaint/FIR filing
- ✅ PDF generation with professional formatting
- ✅ Image and document analysis
- ✅ Location-based police station recommendations
- ✅ IPC section suggestions based on complaint type
- ✅ Google Search integration for real-time information

## 🔐 Security & Privacy

- All conversations are processed securely
- User data is only used for generating documents
- No data is permanently stored
- PDFs are generated locally and deleted after sending

## ⚠️ Important Disclaimers

1. **This is NOT a substitute for professional legal advice**
2. **Consult a lawyer for serious legal matters**
3. **FIR drafts are for reference only - visit police station for official filing**
4. **In emergencies, call 100 or 112 immediately**
5. **The bot provides general information about Indian laws**

## 🤝 Support

For issues or questions about the bot:
- Use `/help` command in the bot
- Check this README for usage instructions

## 📝 License

This project is created for educational and assistance purposes.

## 🎯 Bot Information

- **Bot Username:** @ai_governance_bot
- **Bot Name:** Kakinada Legal Assistant
- **Primary Location:** Kakinada, Andhra Pradesh, India
- **Language:** English
- **AI Model:** Google Gemini Flash with Search Grounding

## 🌟 Key Capabilities

1. **Natural Language Understanding** - Ask questions in plain English
2. **Context-Aware Responses** - Remembers conversation history
3. **Multi-Modal Input** - Text, images, and documents
4. **Interactive Workflows** - Step-by-step guidance
5. **Document Generation** - Professional PDF creation
6. **Location Intelligence** - Kakinada-specific information
7. **Real-time Search** - Up-to-date legal information via Google Search

## 📞 Contact

For the actual bot on Telegram: Search `@ai_governance_bot`

---

**Made with ❤️ for the people of Kakinada and India**

*Stay informed. Stay empowered. Know your rights.*

