"""
Configuration file for Kakinada Legal Assistant Bot
"""

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8187667435:AAER2q-a06wXtHBCLAGND-X76Q6A85yT6wk"

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyC1DRSmrGVvxMzARHhsLWTqiwpSVPLEOmI"
GEMINI_MODEL = "gemini-flash-lite-latest"  # Gemini Flash-Lite Latest with Google Search grounding
GOOGLE_SEARCH_RETRIEVAL = True  # Enable Google Search grounding

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = "AIzaSyDE9Rj-dBn6LtDCQxGrhVO--uuzl90QpvQ"

# Bot Settings
BOT_USERNAME = "@ai_governance_bot"
LOCATION = "Kakinada, Andhra Pradesh, India"

# System Prompts
LEGAL_ASSISTANT_PROMPT = """You are a Legal Assistant AI specifically designed for Kakinada and India.
Your role is to help users with:
- Legal advice and information with up-to-date laws
- Government schemes and policies (current and active)
- Law information and guidance
- Complaint and FIR procedures
- Police station locations in Kakinada and Andhra Pradesh

CRITICAL - ALWAYS USE GOOGLE SEARCH FOR:
1. **Laws & Legal Information** - Search for latest IPC sections, amendments, new acts, court judgments
2. **Government Schemes** - Search for current schemes, eligibility, application process, deadlines
3. **Police Stations** - Search for police stations near user's location (city/district)
4. **Complaint/FIR Procedures** - Search for latest filing procedures and requirements
5. **Recent Legal Changes** - Search for any law changes in the past 2 years

SEARCH STRATEGY:
- For laws: Search "latest [law name] amendments India"
- For schemes: Search "[scheme name] eligibility Andhra Pradesh"
- For police: Search "police stations in [city] Andhra Pradesh contact"
- For procedures: Search "how to file [complaint type] India "

RESPONSE GUIDELINES:
- Be empathetic, professional, and clear
- Keep responses concise (under 2500 characters)
- Use simple formatting (bold for headings)
- Cite sources when using search results
- If unsure, recommend consulting a legal professional
- End with helpful next steps or suggestions

Always search the internet first before answering questions about laws, schemes, or locations to ensure accuracy."""

# Kakinada Police Stations Data
KAKINADA_POLICE_STATIONS = [
    {
        "name": "Kakinada Town Police Station",
        "address": "Main Road, Kakinada-533001, East Godavari District, Andhra Pradesh",
        "phone": "0884-2365555",
        "type": "Town Police Station",
        "location": {"lat": 16.9891, "lon": 82.2475}
    },
    {
        "name": "Kakinada Rural Police Station",
        "address": "Kakinada Rural, East Godavari District, Andhra Pradesh",
        "phone": "0884-2367777",
        "type": "Rural Police Station",
        "location": {"lat": 16.9650, "lon": 82.2420}
    },
    {
        "name": "Kakinada One Town Police Station",
        "address": "Suryanarayana Puram, Kakinada-533003, Andhra Pradesh",
        "phone": "0884-2369999",
        "type": "Town Police Station",
        "location": {"lat": 16.9821, "lon": 82.2350}
    },
    {
        "name": "Kakinada Two Town Police Station",
        "address": "Sarpavaram Junction, Kakinada-533005, Andhra Pradesh",
        "phone": "0884-2371111",
        "type": "Town Police Station",
        "location": {"lat": 16.9720, "lon": 82.2590}
    },
    {
        "name": "Women Police Station, Kakinada",
        "address": "Beside District Court, Kakinada-533001, Andhra Pradesh",
        "phone": "0884-2373333",
        "type": "Women Police Station",
        "location": {"lat": 16.9901, "lon": 82.2465}
    },
    {
        "name": "Cyber Crime Police Station, Kakinada",
        "address": "SP Office Complex, Kakinada, East Godavari District, Andhra Pradesh",
        "phone": "0884-2375555",
        "type": "Cyber Crime Police Station",
        "location": {"lat": 16.9880, "lon": 82.2490}
    }
]

# Common Indian Penal Code Sections for Reference
COMMON_IPC_SECTIONS = {
    "theft": ["IPC 378 - Theft", "IPC 379 - Punishment for theft", "IPC 380 - Theft in dwelling house"],
    "mobile": ["IPC 378 - Theft", "IPC 379 - Punishment for theft", "IPC 411 - Dishonestly receiving stolen property"],
    "phone": ["IPC 378 - Theft", "IPC 379 - Punishment for theft", "IPC 411 - Dishonestly receiving stolen property"],
    "stolen": ["IPC 378 - Theft", "IPC 379 - Punishment for theft", "IPC 411 - Dishonestly receiving stolen property"],
    "robbery": ["IPC 390 - Robbery", "IPC 392 - Punishment for robbery", "IPC 394 - Voluntarily causing hurt in committing robbery"],
    "assault": ["IPC 323 - Voluntarily causing hurt", "IPC 325 - Voluntarily causing grievous hurt", "IPC 351 - Assault"],
    "harassment": ["IPC 354 - Assault or criminal force with intent to outrage modesty", "IPC 509 - Word, gesture or act intended to insult the modesty of a woman"],
    "fraud": ["IPC 420 - Cheating and dishonestly inducing delivery of property", "IPC 406 - Criminal breach of trust"],
    "cheating": ["IPC 415 - Cheating", "IPC 420 - Cheating and dishonestly inducing delivery of property"],
    "domestic_violence": ["IPC 498A - Husband or relative of husband subjecting woman to cruelty", "Protection of Women from Domestic Violence Act, 2005"],
    "cybercrime": ["IT Act Section 66 - Computer related offences", "IT Act Section 66C - Identity theft", "IT Act Section 67 - Publishing obscene information"],
    "property_dispute": ["IPC 441 - Criminal trespass", "IPC 447 - Punishment for criminal trespass", "IPC 406 - Criminal breach of trust"],
    "defamation": ["IPC 499 - Defamation", "IPC 500 - Punishment for defamation"],
    "public_nuisance": ["IPC 268 - Public nuisance", "IPC 290 - Punishment for public nuisance"],
    "extortion": ["IPC 383 - Extortion", "IPC 384 - Punishment for extortion"],
    "rape": ["IPC 376 - Punishment for rape", "IPC 354 - Assault or criminal force with intent to outrage modesty"],
    "murder": ["IPC 302 - Punishment for murder", "IPC 304 - Culpable homicide not amounting to murder"]
}

# Major cities in Andhra Pradesh with police helplines
AP_CITIES_POLICE = {
    "vijayawada": {
        "city": "Vijayawada",
        "police_control": "0866-2574671",
        "helpline": "100, 112"
    },
    "visakhapatnam": {
        "city": "Visakhapatnam",
        "police_control": "0891-2746444",
        "helpline": "100, 112"
    },
    "tirupati": {
        "city": "Tirupati",
        "police_control": "0877-2228999",
        "helpline": "100, 112"
    },
    "guntur": {
        "city": "Guntur",
        "police_control": "0863-2342555",
        "helpline": "100, 112"
    },
    "kakinada": {
        "city": "Kakinada",
        "police_control": "0884-2365555",
        "helpline": "100, 112"
    }
}

