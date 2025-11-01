"""
Kakinada Legal Assistant Telegram Bot
Main bot file with Gemini AI integration
"""
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from google import genai
from google.genai import types
from io import BytesIO
import config
from pdf_generator import create_complaint_pdf

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure Gemini AI with new SDK
client = genai.Client(api_key=config.GEMINI_API_KEY)

# Conversation states for complaint filling
COMPLAINT_NAME, COMPLAINT_FATHER_NAME, COMPLAINT_AGE, COMPLAINT_PHONE, COMPLAINT_EMAIL, COMPLAINT_ADDRESS = range(6)
COMPLAINT_INITIAL_DESC, COMPLAINT_TYPE, COMPLAINT_DATE, COMPLAINT_LOCATION, COMPLAINT_DESCRIPTION = range(6, 11)


class KakinadaLegalBot:
    """Main bot class"""
    
    def __init__(self):
        # Initialize with new Google GenAI SDK that supports Google Search
        self.client = client
        self.model_name = config.GEMINI_MODEL
        
        # Configure Google Search tool
        self.tools = [
            types.Tool(googleSearch=types.GoogleSearch())
        ]
        
        # Generation config
        self.generation_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_output_tokens=2048,
            system_instruction=config.LEGAL_ASSISTANT_PROMPT,
            tools=self.tools
        )
        
        logger.info("✅ Gemini model with Google Search initialized successfully")
        
        # Start chat session
        self.chat_sessions = {}
        self.system_prompt = config.LEGAL_ASSISTANT_PROMPT
    
    def send_message(self, user_id, message):
        """Send message to Gemini with Google Search"""
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)]
            )
        ]
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=self.generation_config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def find_nearest_police_stations(self, complaint_type=None):
        """Find nearest police stations in Kakinada"""
        stations = config.KAKINADA_POLICE_STATIONS
        
        # Filter by type if specified
        if complaint_type:
            complaint_lower = complaint_type.lower()
            if "women" in complaint_lower or "harassment" in complaint_lower:
                women_stations = [s for s in stations if "Women" in s['type']]
                if women_stations:
                    return women_stations
            
            if "cyber" in complaint_lower:
                cyber_stations = [s for s in stations if "Cyber" in s['type']]
                if cyber_stations:
                    return cyber_stations
        
        return stations[:3]  # Return top 3 stations
    
    def get_applicable_laws(self, complaint_type, description=""):
        """Get applicable IPC sections based on complaint type and description"""
        complaint_lower = complaint_type.lower()
        description_lower = description.lower()
        combined_text = complaint_lower + " " + description_lower
        applicable = []
        
        # Check both complaint type and description for keywords
        for key, laws in config.COMMON_IPC_SECTIONS.items():
            if key in combined_text:
                applicable.extend(laws)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_applicable = []
        for law in applicable:
            if law not in seen:
                seen.add(law)
                unique_applicable.append(law)
        
        if unique_applicable:
            return ", ".join(unique_applicable)
        else:
            return "IPC 378/379 (Theft) or other relevant sections - Consult with police for exact applicable sections"
    
    def detect_user_city(self, address, incident_location):
        """Detect which city the user is from"""
        combined = (address + " " + incident_location).lower()
        
        for city_key, city_info in config.AP_CITIES_POLICE.items():
            if city_key in combined or city_info['city'].lower() in combined:
                return city_info
        
        return None
    
    async def send_police_stations(self, update: Update, complaint_type=None):
        """Send police station information"""
        stations = self.find_nearest_police_stations(complaint_type)
        
        message = "🚔 *Nearest Police Stations in Kakinada:*\n\n"
        
        for i, station in enumerate(stations, 1):
            message += f"*{i}. {station['name']}*\n"
            message += f"📍 {station['address']}\n"
            message += f"📞 {station['phone']}\n"
            message += f"🏢 {station['type']}\n\n"
        
        message += "*Emergency Numbers:*\n"
        message += "🚨 Police: 100\n"
        message += "🆘 Emergency: 112\n"
        message += "👮 Women Helpline: 181\n"
        message += "👶 Child Helpline: 1098\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def send_police_stations_callback(self, query):
        """Send police station information for callback query"""
        stations = self.find_nearest_police_stations()
        
        message = "🚔 *Nearest Police Stations in Kakinada:*\n\n"
        
        for i, station in enumerate(stations, 1):
            message += f"*{i}. {station['name']}*\n"
            message += f"📍 {station['address']}\n"
            message += f"📞 {station['phone']}\n"
            message += f"🏢 {station['type']}\n\n"
        
        message += "*Emergency Numbers:*\n"
        message += "🚨 Police: 100\n"
        message += "🆘 Emergency: 112\n"
        message += "👮 Women Helpline: 181\n"
        message += "👶 Child Helpline: 1098\n"
        
        await query.message.reply_text(message, parse_mode='Markdown')


# Initialize bot
legal_bot = KakinadaLegalBot()


# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_message = """🙏 *Namaste! Welcome to Kakinada Legal Assistant* 🏛️

I'm your AI-powered legal assistant for Kakinada and India.

*What I Can Help With:*
📚 Legal Information & Advice
⚖️ Indian Laws & Rights
🏛️ Government Schemes
📝 Complaint/Report Filing (All Types)
📍 Police Station Locations
🔍 Document Analysis

*Quick Commands:*
/help - All commands
/complaint - File complaint/report
/police - Police stations

💬 Ask me anything legal!
📸 Send images/documents for analysis

Choose an option below or ask your question! 👇"""
    
    keyboard = [
        [InlineKeyboardButton("📝 File Complaint/Report", callback_data='start_complaint')],
        [InlineKeyboardButton("📍 Police Stations", callback_data='police_stations')],
        [InlineKeyboardButton("🏛️ Government Schemes", callback_data='gov_schemes'),
         InlineKeyboardButton("⚖️ Legal Info", callback_data='legal_info')],
        [InlineKeyboardButton("💡 Suggested Questions", callback_data='suggestions')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Reset suggestion flag
    context.user_data['suggestion_shown'] = False
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = """🔍 *How to Use Kakinada Legal Assistant*
🌐 *Powered by Google Search - Real-time Information!*

*Commands:*
/start - Start the bot
/help - Show this help message
/complaint - File complaint/report (all types)
/police - Police stations info
/schemes - Government schemes
/laws - Legal information
/cancel - Cancel operation

*What I Can Do:*
✅ Answer legal questions (Latest info)
✅ Explain Indian laws (Up-to-date)
✅ Help with complaint/report filing (all types)
✅ Find police stations (Real-time)
✅ Explain government schemes (Current)
✅ Analyze documents & images
✅ Provide applicable law sections

*How to Ask:*
Just type your question!

Examples:
- "Latest changes in consumer protection law"
- "Current PM Kisan Yojana eligibility 2025"
- "Find police stations in Vijayawada"
- "What is Section 420 IPC?"

*Real-Time Features:*
🔍 Searches Google for latest laws
📅 Gets current government schemes
📍 Finds nearest police stations
⚖️ Checks recent legal amendments

*Document Analysis:*
Send images/documents for analysis!

*Emergency:*
🚨 Police: 100
🆘 Emergency: 112
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def schemes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Government schemes command with structured output"""
    user_id = update.message.from_user.id
    
    await update.message.chat.send_action("typing")
    
    try:
        # Ask AI for current schemes with Google Search
        prompt = """Search Google for the TOP 5 CURRENT government schemes each for:
1. Central Government (India) - 2024
2. Andhra Pradesh State Government - 2024

For each scheme provide:
- Scheme Name
- Brief Purpose (one line)
- Who can apply (one line)

Keep response under 2000 characters. Use ONLY verified, active schemes from official sources."""

        response_text = legal_bot.send_message(user_id, prompt)
        response_text = clean_markdown(response_text)
        
        # Format with header and footer
        formatted_response = f"""🏛️ *Government Schemes - 2024*

{response_text}

---

💡 *Need More Info?*
Ask: "Tell me about [scheme name]"
Example: "Tell me about PM Kisan Yojana"

🔗 *Official Portals:*
• Central: myscheme.gov.in
• AP State: schemes.ap.gov.in

📞 *Helpline:* 1800-XXX-XXXX"""

        if len(formatted_response) > 3800:
            formatted_response = formatted_response[:3700] + "...\n\n💡 Ask for specific schemes!"
        
        try:
            await update.message.reply_text(formatted_response, parse_mode='Markdown')
        except Exception as parse_error:
            logger.error(f"Markdown parse error in schemes: {parse_error}")
            await update.message.reply_text(formatted_response)
            
    except Exception as e:
        logger.error(f"Error in schemes command: {e}")
        fallback = """🏛️ *Popular Government Schemes*

*Central Schemes:*
1. PM-KISAN - Farmer income support
2. Ayushman Bharat - Health insurance
3. PMAY - Housing for all
4. PM SVANidhi - Street vendor loans
5. Digital India - Digital empowerment

*AP State Schemes:*
1. YSR Cheyutha - Women empowerment
2. Rythu Bharosa - Farmer assistance
3. Amma Vodi - Education support
4. Jagananna Thodu - Small business loans
5. YSR Pension - Social security

💡 Ask: "Tell me about [scheme name]" for details!"""
        await update.message.reply_text(fallback, parse_mode='Markdown')


async def laws_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Legal information command with structured output"""
    user_id = update.message.from_user.id
    
    await update.message.chat.send_action("typing")
    
    try:
        # Ask AI for legal rights overview with Google Search
        prompt = """Provide a clean, structured overview of Fundamental Rights in India:

List the 6 main categories of Fundamental Rights (Articles 12-35) with:
- Article numbers
- Brief description (one line each)

Also mention 3 important legal rights every citizen should know.

Keep under 2000 characters. Use official Constitution sources."""

        response_text = legal_bot.send_message(user_id, prompt)
        response_text = clean_markdown(response_text)
        
        # Format with header and footer
        formatted_response = f"""⚖️ *Legal Rights in India*

{response_text}

---

💡 *Common Legal Questions:*
• "What is Section 498A IPC?"
• "What are consumer rights?"
• "How to file an FIR?"
• "What is the RTI Act?"

📞 *Legal Helplines:*
• National Legal Services: 15100
• Women Helpline: 1091
• Police: 100

🔍 *Need Legal Advice?*
Ask me about specific laws or your situation!"""

        if len(formatted_response) > 3800:
            formatted_response = formatted_response[:3700] + "...\n\n💡 Ask for specific laws!"
        
        try:
            await update.message.reply_text(formatted_response, parse_mode='Markdown')
        except Exception as parse_error:
            logger.error(f"Markdown parse error in laws: {parse_error}")
            await update.message.reply_text(formatted_response)
            
    except Exception as e:
        logger.error(f"Error in laws command: {e}")
        fallback = """⚖️ *Fundamental Rights in India*

*6 Main Categories:*

1️⃣ *Right to Equality* (Art. 14-18)
   Equality before law, no discrimination

2️⃣ *Right to Freedom* (Art. 19-22)
   Speech, assembly, movement, profession

3️⃣ *Right Against Exploitation* (Art. 23-24)
   No forced labor, no child labor

4️⃣ *Right to Freedom of Religion* (Art. 25-28)
   Practice any religion freely

5️⃣ *Cultural & Educational Rights* (Art. 29-30)
   Protect minority rights

6️⃣ *Right to Constitutional Remedies* (Art. 32-35)
   Enforce your rights in court

---

*Other Important Rights:*
✅ Right to Free Legal Aid
✅ Right to File FIR
✅ Right to Privacy
✅ Right to Remain Silent

💡 Ask: "Tell me about [specific law]" for details!"""
        await update.message.reply_text(fallback, parse_mode='Markdown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_complaint':
        await query.message.reply_text("📝 Starting complaint/report filing process...\n\nUse /complaint command to begin")
    elif query.data == 'police_stations':
        await legal_bot.send_police_stations_callback(query)
    elif query.data == 'gov_schemes':
        # Create temporary message to send to AI
        context.user_data['temp_message'] = "Tell me about major government schemes in India and Andhra Pradesh (brief overview)"
        # Simulate a message update
        await handle_message_for_callback(query, context)
    elif query.data == 'legal_info':
        context.user_data['temp_message'] = "Give me an overview of common legal rights in India (brief)"
        await handle_message_for_callback(query, context)
    elif query.data == 'suggestions':
        # Show suggested questions with keyboard
        keyboard = [
            ["What are my tenant rights?"],
            ["How to file consumer complaint?"],
            ["What is POCSO Act?"],
            ["Tell me about PM Kisan Yojana"],
            ["What is Section 498A IPC?"],
            ["How to get police protection?"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await query.message.reply_text(
            "💡 *Here are some questions you can ask:*\n\nTap any question below or type your own!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def handle_message_for_callback(query, context):
    """Helper to handle callback query messages"""
    user_message = context.user_data.get('temp_message', '')
    if user_message:
        user_id = query.from_user.id
        
        try:
            response_text = legal_bot.send_message(user_id, user_message)
            
            # Truncate if too long
            if len(response_text) > 4000:
                response_text = response_text[:3900] + "...\n\n(Response truncated. Ask for specific details!)"
            
            try:
                await query.message.reply_text(response_text, parse_mode='Markdown')
            except:
                # Fallback to plain text
                await query.message.reply_text(response_text)
        except Exception as e:
            await query.message.reply_text(f"I can help you with: {user_message}\n\nPlease ask me directly!")


async def police_stations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show nearest police stations - request user's location"""
    # Create location request button
    from telegram import KeyboardButton, ReplyKeyboardMarkup
    
    location_button = KeyboardButton(
        text="📍 Share My Location",
        request_location=True
    )
    
    keyboard = ReplyKeyboardMarkup(
        [[location_button], ["❌ Cancel"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    response = """📍 *Find Nearest Police Stations*

To show you the nearest police stations, I need your current location.

👇 *Click the button below* to share your location, or type your city/area name.

Your location data is used only to find nearby police stations and is not stored."""
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown',
        reply_markup=keyboard
    )


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle location shared by user - Uses Google Maps Places API"""
    from telegram import ReplyKeyboardRemove
    import googlemaps
    from datetime import datetime
    import math
    
    location = update.message.location
    
    if not location:
        await update.message.reply_text(
            "❌ Location not received. Please try again or type your city name.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    latitude = location.latitude
    longitude = location.longitude
    
    await update.message.reply_text(
        f"📍 Location received!\n🔍 Searching for nearest police stations using Google Maps...",
        reply_markup=ReplyKeyboardRemove()
    )
    
    try:
        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)
        
        # Search for police stations near the coordinates
        places_result = gmaps.places_nearby(
            location=(latitude, longitude),
            radius=5000,  # Search within 5km radius
            type='police',
            keyword='police station'
        )
        
        if not places_result.get('results'):
            await update.message.reply_text(
                "❌ No police stations found near your location.\n\n"
                "📞 Emergency: 100 | 112\n\n"
                "💡 Try typing your city name instead.",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        
        # Get top 3 nearest police stations
        police_stations = places_result['results'][:3]
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            """Calculate distance between two coordinates using Haversine formula"""
            R = 6371  # Radius of Earth in kilometers
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            distance = R * c
            return round(distance, 2)
        
        # Format the response
        response_parts = ["📍 *Nearest Police Stations to Your Location:*\n"]
        
        for idx, station in enumerate(police_stations, 1):
            name = station.get('name', 'Unknown Police Station')
            address = station.get('vicinity', 'Address not available')
            
            # Get place details for phone number
            place_id = station.get('place_id')
            try:
                place_details = gmaps.place(place_id=place_id, fields=['formatted_phone_number', 'international_phone_number'])
                phone = place_details.get('result', {}).get('formatted_phone_number') or \
                        place_details.get('result', {}).get('international_phone_number') or \
                        "Not available"
            except:
                phone = "Not available"
            
            # Calculate distance
            station_lat = station['geometry']['location']['lat']
            station_lon = station['geometry']['location']['lng']
            distance = calculate_distance(latitude, longitude, station_lat, station_lon)
            
            # Build station info
            station_info = f"""
{idx}. *{name}*
📍 Address: {address}
📞 Phone: {phone}
🚗 Distance: {distance} km
"""
            response_parts.append(station_info)
        
        response_parts.append("""
---
🚨 *Emergency Numbers:*
📞 Police: 100 | 🆘 Emergency: 112

💡 *Tip:* Save these numbers for quick access!
""")
        
        response = "\n".join(response_parts)
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error finding police stations by location: {e}")
        await update.message.reply_text(
            f"❌ Sorry, I couldn't find police stations near your location.\n\n"
            f"📞 Emergency: 100 | 112\n\n"
            f"💡 Try typing your city name instead.\n\n"
            f"Error: {str(e)}",
            reply_markup=ReplyKeyboardRemove()
        )


# Complaint filing conversation handlers
async def complaint_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start complaint filing"""
    await update.message.reply_text(
        "📝 *Complaint Filing Assistant*\n\n"
        "I'll help you prepare a complaint. Please answer the following questions.\n\n"
        "Let's start with your personal details:\n\n"
        "*What is your full name?*",
        parse_mode='Markdown'
    )
    context.user_data['complaint'] = {}
    return COMPLAINT_NAME


async def complaint_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get complainant name"""
    context.user_data['complaint']['name'] = update.message.text
    await update.message.reply_text("*What is your Father's/Husband's name?*", parse_mode='Markdown')
    return COMPLAINT_FATHER_NAME


async def complaint_father_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get father's name"""
    context.user_data['complaint']['father_name'] = update.message.text
    await update.message.reply_text("*What is your age?*", parse_mode='Markdown')
    return COMPLAINT_AGE


async def complaint_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get age"""
    context.user_data['complaint']['age'] = update.message.text
    await update.message.reply_text("*What is your phone number?*", parse_mode='Markdown')
    return COMPLAINT_PHONE


async def complaint_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get phone number"""
    context.user_data['complaint']['phone'] = update.message.text
    await update.message.reply_text("*What is your email address?* (Optional - type 'skip' to skip)", parse_mode='Markdown')
    return COMPLAINT_EMAIL


async def complaint_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get email"""
    email = update.message.text
    if email.lower() != 'skip':
        context.user_data['complaint']['email'] = email
    
    await update.message.reply_text(
        "*What is your complete address?*\n\n"
        "Please include:\n"
        "• House/Street details\n"
        "• Village/Town/City\n"
        "• Mandal\n"
        "• District\n\n"
        "Example: 'Door No 12-34, MG Road, Vijayawada, Vijayawada Mandal, Krishna District'",
        parse_mode='Markdown'
    )
    return COMPLAINT_ADDRESS


async def complaint_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get address"""
    context.user_data['complaint']['address'] = update.message.text
    await update.message.reply_text(
        "*Please describe what happened to you:*\n\n"
        "Explain the incident in your own words. The bot will understand and suggest the complaint type.\n\n"
        "Example: 'Someone stole my mobile phone from my bag'",
        parse_mode='Markdown'
    )
    return COMPLAINT_INITIAL_DESC


async def complaint_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get complaint type confirmation or custom input"""
    user_input = update.message.text.strip()
    
    if user_input.lower() in ['yes', 'correct', 'ok', 'y', 'yeah', 'right']:
        # User confirmed the AI suggestion
        complaint_type = context.user_data['complaint'].get('suggested_type', user_input)
    elif user_input.lower() == 'skip':
        complaint_type = "General Complaint"
    else:
        # User typed their own complaint type
        complaint_type = user_input
    
    context.user_data['complaint']['complaint_type'] = complaint_type
    await update.message.reply_text("*When did the incident occur? (Date and time)*", parse_mode='Markdown')
    return COMPLAINT_DATE


async def complaint_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get incident date"""
    context.user_data['complaint']['incident_date'] = update.message.text
    await update.message.reply_text(
        "*Where did the incident occur? (Location/Address)*\n\n"
        "Include: Area/Landmark, City/Village, Mandal, District\n\n"
        "Example: 'Near Railway Station, Vijayawada, Vijayawada Mandal, Krishna District'",
        parse_mode='Markdown'
    )
    return COMPLAINT_LOCATION


async def complaint_initial_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get initial incident description and auto-detect complaint type"""
    description = update.message.text
    context.user_data['complaint']['initial_description'] = description
    
    # Show analyzing message
    await update.message.reply_text("🤔 Analyzing your complaint...", parse_mode='Markdown')
    
    try:
        # Use AI to detect complaint type
        analysis_prompt = f"""Based on this incident description, identify the most appropriate complaint type.

Description: "{description}"

Analyze and respond with ONLY the complaint type in this format:
Type: [complaint type]

Choose from: Theft, Robbery, Fraud, Cheating, Harassment, Cyber Crime, Domestic Violence, Property Dispute, Assault, Kidnapping, Missing Person, Traffic Violation, Forgery, or suggest appropriate type.

Keep it concise - just the type name."""

        user_id = update.message.from_user.id
        ai_response = legal_bot.send_message(user_id, analysis_prompt)
        
        # Extract complaint type from AI response
        complaint_type = ai_response.strip()
        if "Type:" in complaint_type:
            complaint_type = complaint_type.split("Type:")[1].strip()
        
        # Clean up the response
        complaint_type = complaint_type.split('\n')[0].strip()
        
        context.user_data['complaint']['suggested_type'] = complaint_type
        
        # Ask for confirmation
        await update.message.reply_text(
            f"✅ *I understand this is about:*\n\n"
            f"📋 **{complaint_type}**\n\n"
            f"Is this correct?\n"
            f"• Type *'yes'* to confirm\n"
            f"• Type the correct complaint type (e.g., 'Theft', 'Fraud')\n"
            f"• Type *'skip'* if you're not sure",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in auto-detecting complaint type: {e}")
        await update.message.reply_text(
            "*What type of complaint is this?*\n\n"
            "Examples: Theft, Fraud, Harassment, Property Dispute\n"
            "Or type 'skip' if not sure",
            parse_mode='Markdown'
        )
    
    return COMPLAINT_TYPE


async def complaint_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get incident location"""
    context.user_data['complaint']['incident_location'] = update.message.text
    await update.message.reply_text(
        "*Any additional details you want to add?*\n\n"
        "Include witnesses, evidence, sequence of events, etc.\n"
        "Or type 'no' to skip",
        parse_mode='Markdown'
    )
    return COMPLAINT_DESCRIPTION


async def complaint_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process additional details and generate PDF"""
    additional_details = update.message.text
    
    # Combine initial description with additional details
    initial_desc = context.user_data['complaint'].get('initial_description', '')
    
    if additional_details.lower() in ['no', 'skip', 'none']:
        final_description = initial_desc
    else:
        final_description = f"{initial_desc}\n\nAdditional Details: {additional_details}"
    
    context.user_data['complaint']['description'] = final_description
    
    await update.message.reply_text("⏳ Processing your complaint... Please wait.\n🤖 Analyzing incident details...")
    
    complaint_data = context.user_data['complaint']
    
    # Safety check for complaint_type
    complaint_type = complaint_data.get('complaint_type', 'General Complaint')
    description = complaint_data['description']
    address = complaint_data['address']
    incident_location = complaint_data['incident_location']
    
    # Get applicable laws (now includes description analysis)
    applicable_laws = legal_bot.get_applicable_laws(complaint_type, description)
    complaint_data['applicable_laws'] = applicable_laws
    
    # Use Google Search to find nearest police stations based on incident location
    await update.message.reply_text("🔍 Searching for nearest police stations in your area...")
    
    try:
        user_id = update.message.from_user.id
        
        # Ask AI to search for nearest police stations
        police_search_prompt = f"""Search Google for police stations with jurisdiction over this complaint:

Incident Location: {incident_location}
User Address: {address}  
Complaint Type: {complaint_type}

Provide ONLY the following in a clean format:

**Police Station Name**
📍 Address: [Full address with mandal, district, pincode]
📞 Phone: [Contact number]
✅ Jurisdiction: [Brief - covers this area for {complaint_type} cases]

If there are 2 stations (one for incident, one for residence), list both clearly.

Keep it SHORT and CLEAN. No explanations. Just facts."""

        police_response = legal_bot.send_message(user_id, police_search_prompt)
        
        # Extract clean police station name for PDF
        # Take first line or first station name
        police_lines = police_response.strip().split('\n')
        clean_police_name = police_lines[0].replace('**', '').replace('*', '').strip()
        if clean_police_name.startswith('#'):
            clean_police_name = police_lines[1].replace('**', '').replace('*', '').strip() if len(police_lines) > 1 else "Police Station"
        
        # Clean and format the response
        police_info = f"""
📍 *Police Station Information:*

{police_response}

---
🚨 *Emergency Numbers:*
📞 Police: 100 | 🆘 Emergency: 112
"""
        
        complaint_data['police_station'] = clean_police_name  # Clean name for PDF
        complaint_data['police_details'] = police_response  # Full details for reference
        
    except Exception as e:
        logger.error(f"Error searching for police stations: {e}")
        # Fallback to generic message
        police_info = f"""
📍 *Police Station Information:*

Please visit the nearest police station in your area:
📍 Location: {incident_location}

To find your nearest police station, search online or dial 100 for police assistance.

🚨 *Emergency Numbers:*
📞 Police: 100
🆘 Emergency: 112
"""
        complaint_data['police_station'] = f"Nearest station in {incident_location}"
    
    # Generate PDF
    try:
        filename = f"complaint_{update.message.from_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = create_complaint_pdf(complaint_data, filename)
        
        # Send summary
        summary = f"""
✅ *Complaint Form Generated Successfully!*

👤 *Complainant:* {complaint_data['name']}
📋 *Type:* {complaint_type}
📍 *Location:* {incident_location}

⚖️ *Applicable Laws:*
{applicable_laws}

{police_info}

💡 *Next Steps:*
1️⃣ Visit the police station immediately
2️⃣ Carry this complaint form (PDF below)
3️⃣ Bring evidence (CCTV, documents, witnesses)
4️⃣ Note FIR number after filing

📄 *Your complaint PDF is ready below* ⬇️
"""
        
        await update.message.reply_text(summary, parse_mode='Markdown')
        
        # Send PDF
        with open(pdf_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename=filename,
                caption="📄 Your complaint form is ready!\n\n"
                        "⚠️ Please review carefully and submit at your LOCAL police station.\n"
                        "💡 Carry original documents and evidence.\n"
                        "🚨 For emergency, dial 100 or 112"
            )
        
        # Clean up
        os.remove(pdf_path)
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        await update.message.reply_text("❌ Sorry, there was an error generating the PDF. Please try again.")
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current operation"""
    await update.message.reply_text(
        "❌ Operation cancelled.\n\nUse /start to begin again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def clean_markdown(text):
    """Clean and fix markdown formatting for Telegram"""
    import re
    
    # Remove excessive asterisks and fix bold formatting
    text = re.sub(r'\*\*\*+', '**', text)  # Triple+ asterisks to double
    text = re.sub(r'(?<!\*)\*(?!\*)', '', text)  # Remove single asterisks
    
    # Fix headings - convert ## to bold
    text = re.sub(r'###\s+(.+?)$', r'*\1*', text, flags=re.MULTILINE)
    text = re.sub(r'##\s+(.+?)$', r'*\1*', text, flags=re.MULTILINE)
    text = re.sub(r'#\s+(.+?)$', r'*\1*', text, flags=re.MULTILINE)
    
    # Clean up extra spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


async def send_suggested_questions(update: Update, topic="general"):
    """Send suggested questions to user"""
    suggestions = {
        "general": [
            "What are my tenant rights?",
            "How to file consumer complaint?",
            "What is Right to Information Act?",
            "Tell me about government schemes"
        ],
        "law": [
            "What is Section 498A IPC?",
            "Explain dowry prohibition law",
            "What is POCSO Act?",
            "Tell me about bail procedures"
        ],
        "schemes": [
            "PM Kisan Yojana details",
            "Ayushman Bharat scheme",
            "Pension schemes in India",
            "Housing schemes in AP"
        ]
    }
    
    questions = suggestions.get(topic, suggestions["general"])
    keyboard = [[q] for q in questions]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "💡 *Suggested Questions:*\nTap on any question below:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages with Gemini AI"""
    user_message = update.message.text
    user_id = update.message.from_user.id
    
    # Show typing indicator
    await update.message.chat.send_action("typing")
    
    try:
        # Add context about Kakinada
        contextualized_message = f"""{user_message}

[Context: User is from Kakinada, Andhra Pradesh, India. 
Instructions: 
- Keep response concise (under 2500 characters)
- Use simple formatting (bold for headings)
- Be clear and easy to understand
- End with a helpful suggestion if relevant]"""
        
        # Send message to Gemini with Google Search
        response_text = legal_bot.send_message(user_id, contextualized_message)
        
        # Clean markdown
        response_text = clean_markdown(response_text)
        
        # Split message if too long (Telegram limit is 4096 characters)
        max_length = 3800
        if len(response_text) > max_length:
            # Split into chunks at paragraph breaks
            paragraphs = response_text.split('\n\n')
            chunks = []
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) + 2 < max_length:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para + "\n\n"
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Send chunks
            for i, chunk in enumerate(chunks):
                try:
                    await update.message.reply_text(chunk, parse_mode='Markdown')
                except:
                    # Fallback to plain text if markdown fails
                    await update.message.reply_text(chunk)
                
                # Add "continued..." for multi-part messages
                if i < len(chunks) - 1:
                    await update.message.reply_text("_(continued...)_", parse_mode='Markdown')
        else:
            # Send single message
            try:
                await update.message.reply_text(response_text, parse_mode='Markdown')
            except Exception as e:
                # Fallback to plain text if markdown fails
                logger.warning(f"Markdown parse failed, sending as plain text: {e}")
                # Remove all markdown
                plain_text = response_text.replace('*', '').replace('_', '').replace('`', '')
                await update.message.reply_text(plain_text)
        
        # Show suggested questions periodically
        if not context.user_data.get('suggestion_shown', False):
            # Determine topic based on keywords
            topic = "general"
            if any(word in user_message.lower() for word in ['law', 'ipc', 'section', 'act', 'legal']):
                topic = "law"
            elif any(word in user_message.lower() for word in ['scheme', 'yojana', 'benefit', 'pension']):
                topic = "schemes"
            
            await send_suggested_questions(update, topic)
            context.user_data['suggestion_shown'] = True
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "I apologize, I'm having trouble processing your request. "
            "Please try rephrasing or use one of the commands:\n"
            "/help - Show available commands\n"
            "/complaint - File complaint/report\n"
            "/police - Find police stations"
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    await update.message.reply_text("📸 Analyzing your image... Please wait.")
    
    try:
        # Get the largest photo
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # Download photo
        photo_bytes = await file.download_as_bytearray()
        
        # Process with Gemini Vision
        user_id = update.message.from_user.id
        
        # Get caption if provided
        caption = update.message.caption or "Analyze this legal document or image and provide relevant information."
        
        # Add context
        prompt = f"{caption}\n\n[Context: This is for legal assistance in Kakinada, India. Provide relevant legal information if applicable.]"
        
        # For now, text-only response (image support needs different implementation in new SDK)
        response_text = f"📋 *Image Received*\n\n{caption}\n\nNote: Full image analysis coming soon with updated SDK."
        
        # Handle long responses
        if len(response_text) > 4000:
            response_text = response_text[:3900] + "...\n\n(Response truncated)"
        
        try:
            await update.message.reply_text(response_text, parse_mode='Markdown')
        except:
            # Fallback to plain text
            await update.message.reply_text(response_text)
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't analyze the image. Please try again or send a text description.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages"""
    await update.message.reply_text("📄 Analyzing your document... Please wait.")
    
    try:
        document = update.message.document
        file = await context.bot.get_file(document.file_id)
        
        # Download document
        doc_bytes = await file.download_as_bytearray()
        
        # For now, inform user about document type
        await update.message.reply_text(
            f"📄 Document received: {document.file_name}\n\n"
            "I can help analyze legal documents. Please describe what you need help with regarding this document, "
            "or ask specific questions about it."
        )
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process the document. Please try again.")


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("police", police_stations))
    application.add_handler(CommandHandler("schemes", schemes_command))
    application.add_handler(CommandHandler("laws", laws_command))
    
    # Location handler (must be before general message handler)
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Complaint filing conversation
    complaint_handler = ConversationHandler(
        entry_points=[CommandHandler("complaint", complaint_start)],
        states={
            COMPLAINT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_name)],
            COMPLAINT_FATHER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_father_name)],
            COMPLAINT_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_age)],
            COMPLAINT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_phone)],
            COMPLAINT_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_email)],
            COMPLAINT_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_address)],
            COMPLAINT_INITIAL_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_initial_description)],
            COMPLAINT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_type)],
            COMPLAINT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_date)],
            COMPLAINT_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_location)],
            COMPLAINT_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, complaint_description)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(complaint_handler)
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("🚀 Kakinada Legal Assistant Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

