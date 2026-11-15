
import os
import sqlite3
import hashlib
import secrets
import json
from datetime import date, datetime
from io import BytesIO

import streamlit as st
from openai import OpenAI

# ==================================================
# CARELOOP CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Careloop",
    page_icon="💜",
    layout="wide"
)

DB = "careloop.db"
CHAT_MODEL = "gpt-6-luna"
TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
TTS_MODEL = "gpt-4o-mini-tts"

LANGUAGES = {
    "English": "English",
    "ಕನ್ನಡ (Kannada)": "Kannada",
    "हिन्दी (Hindi)": "Hindi",
    "தமிழ் (Tamil)": "Tamil",
    "తెలుగు (Telugu)": "Telugu",
    "മലയാളം (Malayalam)": "Malayalam",
    "বাংলা (Bengali)": "Bengali",
    "मराठी (Marathi)": "Marathi",
    "ગુજરાતી (Gujarati)": "Gujarati",
    "ਪੰਜਾਬੀ (Punjabi)": "Punjabi",
    "العربية (Arabic)": "Arabic",
    "Français (French)": "French",
    "Español (Spanish)": "Spanish",
    "Deutsch (German)": "German",
    "日本語 (Japanese)": "Japanese"
}

# ==================================================
# TRANSLATIONS
# ==================================================

# Each language has the same translation keys.
# If a translation is missing, English is used as fallback.

ENGLISH = {
    "dashboard": "Dashboard",
    "companion": "AI Companion",
    "quiz": "Quick Quiz",
    "reminders": "Reminders",
    "profile": "Profile",
    "logout": "Log out",
    "language": "Choose language",
    "menu": "Menu",
    "welcome": "Your everyday care starts here.",
    "companion_desc": "Talk, ask questions and get support.",
    "quiz_desc": "Learn something new every day.",
    "reminder_desc": "Keep track of important tasks.",
    "send": "Send",
    "message": "Type your message...",
    "thinking": "Careloop is thinking...",
    "speak": "Speak to Careloop",
    "record": "Record your voice",
    "transcribe": "Transcribe and send",
    "listening": "Listening...",
    "hear": "Hear Careloop speak",
    "generate_voice": "Generate spoken reply",
    "clear_chat": "Clear conversation",
    "topic": "What topic would you like to practise?",
    "difficulty": "Difficulty",
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
    "generate_quiz": "Generate quiz",
    "check_answers": "Check answers",
    "choose_answer": "Choose an answer",
    "score": "Your score",
    "reminder": "Reminder",
    "date": "Date",
    "add_reminder": "Add reminder",
    "delete": "Delete",
    "no_reminders": "No reminders yet.",
    "saved": "Reminder saved.",
    "name": "Name",
    "email": "Email",
    "login": "Login",
    "register": "Register",
    "password": "Password",
    "create_account": "Create account",
    "logout_confirm": "Log out",
    "welcome_back": "Welcome back",
    "incorrect_login": "Incorrect email or password.",
    "enter_topic": "Enter a topic.",
    "correct": "Correct!",
    "your_name": "Your name",
    "chat_caption": "Chat with Careloop using text or your microphone.",
    "microphone_caption": "Allow microphone access when your browser asks.",
    "profile_info": "Your account information",
    "account_created": "Account created successfully. You can now log in.",
    "email_exists": "This email is already registered. Please log in.",
    "valid_details": "Enter a valid name and email.",
    "password_length": "Password must have at least 8 characters.",
    "no_speech": "No speech detected.",
    "api_missing": "OpenAI API key not found. Check .streamlit/secrets.toml.",
    "login_first": "Please log in to continue."
}

TRANSLATIONS = {
    "English": ENGLISH,

    "Kannada": {
        **ENGLISH,
        "dashboard": "ಮುಖಪುಟ",
        "companion": "AI ಸಹಾಯಕ",
        "quiz": "ತ್ವರಿತ ರಸಪ್ರಶ್ನೆ",
        "reminders": "ಜ್ಞಾಪನೆಗಳು",
        "profile": "ಪ್ರೊಫೈಲ್",
        "logout": "ಲಾಗ್ ಔಟ್",
        "language": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "menu": "ಮೆನು",
        "welcome": "ನಿಮ್ಮ ದೈನಂದಿನ ಆರೈಕೆ ಇಲ್ಲಿಂದ ಪ್ರಾರಂಭವಾಗುತ್ತದೆ.",
        "send": "ಕಳುಹಿಸಿ",
        "message": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಬರೆಯಿರಿ...",
        "thinking": "Careloop ಯೋಚಿಸುತ್ತಿದೆ...",
        "speak": "Careloop ಜೊತೆ ಮಾತನಾಡಿ",
        "record": "ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ರೆಕಾರ್ಡ್ ಮಾಡಿ",
        "transcribe": "ಪಠ್ಯವಾಗಿ ಪರಿವರ್ತಿಸಿ ಮತ್ತು ಕಳುಹಿಸಿ",
        "generate_quiz": "ರಸಪ್ರಶ್ನೆ ರಚಿಸಿ",
        "difficulty": "ಕಷ್ಟದ ಮಟ್ಟ",
        "easy": "ಸುಲಭ",
        "medium": "ಮಧ್ಯಮ",
        "hard": "ಕಠಿಣ",
        "reminder": "ಜ್ಞಾಪನೆ",
        "date": "ದಿನಾಂಕ",
        "add_reminder": "ಜ್ಞಾಪನೆ ಸೇರಿಸಿ",
        "delete": "ಅಳಿಸಿ",
        "no_reminders": "ಇನ್ನೂ ಯಾವುದೇ ಜ್ಞಾಪನೆಗಳಿಲ್ಲ.",
        "saved": "ಜ್ಞಾಪನೆ ಉಳಿಸಲಾಗಿದೆ.",
        "name": "ಹೆಸರು",
        "email": "ಇಮೇಲ್",
        "login": "ಲಾಗಿನ್",
        "register": "ನೋಂದಣಿ",
        "password": "ಪಾಸ್‌ವರ್ಡ್",
        "create_account": "ಖಾತೆ ರಚಿಸಿ",
        "correct": "ಸರಿಯಾಗಿದೆ!",
        "choose_answer": "ಉತ್ತರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "check_answers": "ಉತ್ತರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ",
        "score": "ನಿಮ್ಮ ಅಂಕ",
        "your_name": "ನಿಮ್ಮ ಹೆಸರು",
        "account_created": "ಖಾತೆ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ.",
        "enter_topic": "ಒಂದು ವಿಷಯವನ್ನು ನಮೂದಿಸಿ."
    },

    "Hindi": {
        **ENGLISH,
        "dashboard": "डैशबोर्ड",
        "companion": "AI साथी",
        "quiz": "क्विज़",
        "reminders": "रिमाइंडर",
        "profile": "प्रोफ़ाइल",
        "logout": "लॉग आउट",
        "language": "भाषा चुनें",
        "menu": "मेनू",
        "welcome": "आपकी रोज़मर्रा की देखभाल यहीं से शुरू होती है।",
        "send": "भेजें",
        "message": "अपना संदेश लिखें...",
        "thinking": "Careloop सोच रहा है...",
        "speak": "Careloop से बात करें",
        "record": "अपनी आवाज़ रिकॉर्ड करें",
        "transcribe": "लिखित रूप में बदलें और भेजें",
        "generate_quiz": "क्विज़ बनाएँ",
        "difficulty": "कठिनाई",
        "easy": "आसान",
        "medium": "मध्यम",
        "hard": "कठिन",
        "reminder": "रिमाइंडर",
        "date": "तारीख",
        "add_reminder": "रिमाइंडर जोड़ें",
        "delete": "हटाएँ",
        "no_reminders": "अभी कोई रिमाइंडर नहीं है।",
        "saved": "रिमाइंडर सेव हो गया।",
        "name": "नाम",
        "email": "ईमेल",
        "login": "लॉगिन",
        "register": "रजिस्टर",
        "password": "पासवर्ड",
        "create_account": "खाता बनाएँ",
        "correct": "सही!",
        "choose_answer": "उत्तर चुनें",
        "check_answers": "उत्तर जाँचें",
        "score": "आपका स्कोर",
        "your_name": "आपका नाम",
        "account_created": "खाता सफलतापूर्वक बनाया गया।",
        "enter_topic": "एक विषय दर्ज करें।"
    },

    "Tamil": {
        **ENGLISH,
        "dashboard": "முகப்பு",
        "companion": "AI துணைவர்",
        "quiz": "வினாடி வினா",
        "reminders": "நினைவூட்டல்கள்",
        "profile": "சுயவிவரம்",
        "logout": "வெளியேறு",
        "language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "menu": "மெனு",
        "welcome": "உங்கள் அன்றாட பராமரிப்பு இங்கே தொடங்குகிறது.",
        "send": "அனுப்பு",
        "message": "உங்கள் செய்தியை எழுதுங்கள்...",
        "thinking": "Careloop யோசிக்கிறது...",
        "speak": "Careloop உடன் பேசுங்கள்",
        "record": "உங்கள் குரலைப் பதிவு செய்யுங்கள்",
        "generate_quiz": "வினாடி வினாவை உருவாக்கு",
        "difficulty": "கடின நிலை",
        "easy": "எளிது",
        "medium": "நடுத்தரம்",
        "hard": "கடினம்",
        "reminder": "நினைவூட்டல்",
        "date": "தேதி",
        "add_reminder": "நினைவூட்டலைச் சேர்",
        "delete": "நீக்கு",
        "no_reminders": "நினைவூட்டல்கள் எதுவும் இல்லை.",
        "saved": "நினைவூட்டல் சேமிக்கப்பட்டது.",
        "name": "பெயர்",
        "email": "மின்னஞ்சல்",
        "login": "உள்நுழை",
        "register": "பதிவு செய்",
        "password": "கடவுச்சொல்",
        "create_account": "கணக்கை உருவாக்கு",
        "correct": "சரி!",
        "choose_answer": "பதிலைத் தேர்ந்தெடுக்கவும்",
        "check_answers": "பதில்களைச் சரிபார்க்கவும்",
        "score": "உங்கள் மதிப்பெண்"
    },

    "Telugu": {
        **ENGLISH,
        "dashboard": "డాష్‌బోర్డ్",
        "companion": "AI సహచరుడు",
        "quiz": "క్విజ్",
        "reminders": "రిమైండర్లు",
        "profile": "ప్రొఫైల్",
        "logout": "లాగ్ అవుట్",
        "language": "భాషను ఎంచుకోండి",
        "menu": "మెనూ",
        "welcome": "మీ రోజువారీ సంరక్షణ ఇక్కడ ప్రారంభమవుతుంది.",
        "send": "పంపండి",
        "message": "మీ సందేశాన్ని రాయండి...",
        "thinking": "Careloop ఆలోచిస్తోంది...",
        "speak": "Careloopతో మాట్లాడండి",
        "record": "మీ వాయిస్‌ను రికార్డ్ చేయండి",
        "generate_quiz": "క్విజ్ రూపొందించండి",
        "difficulty": "కఠినత",
        "easy": "సులభం",
        "medium": "మధ్యస్థం",
        "hard": "కష్టం",
        "reminder": "రిమైండర్",
        "date": "తేదీ",
        "add_reminder": "రిమైండర్ జోడించండి",
        "delete": "తొలగించండి",
        "no_reminders": "ఇంకా రిమైండర్లు లేవు.",
        "saved": "రిమైండర్ సేవ్ చేయబడింది.",
        "name": "పేరు",
        "email": "ఇమెయిల్",
        "login": "లాగిన్",
        "register": "నమోదు",
        "password": "పాస్‌వర్డ్",
        "create_account": "ఖాతా సృష్టించండి"
    },

    "Malayalam": {
        **ENGLISH,
        "dashboard": "ഡാഷ്ബോർഡ്",
        "companion": "AI കൂട്ടുകാരൻ",
        "quiz": "ക്വിസ്",
        "reminders": "ഓർമ്മപ്പെടുത്തലുകൾ",
        "profile": "പ്രൊഫൈൽ",
        "logout": "ലോഗ് ഔട്ട്",
        "language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "menu": "മെനു",
        "welcome": "നിങ്ങളുടെ ദൈനംദിന പരിചരണം ഇവിടെ ആരംഭിക്കുന്നു.",
        "send": "അയയ്ക്കുക",
        "message": "നിങ്ങളുടെ സന്ദേശം എഴുതുക...",
        "thinking": "Careloop ചിന്തിക്കുന്നു...",
        "generate_quiz": "ക്വിസ് സൃഷ്ടിക്കുക",
        "difficulty": "കാഠിന്യം",
        "easy": "എളുപ്പം",
        "medium": "ഇടത്തരം",
        "hard": "കഠിനം",
        "reminder": "ഓർമ്മപ്പെടുത്തൽ",
        "date": "തീയതി",
        "add_reminder": "ഓർമ്മപ്പെടുത്തൽ ചേർക്കുക",
        "delete": "ഇല്ലാതാക്കുക",
        "no_reminders": "ഓർമ്മപ്പെടുത്തലുകൾ ഒന്നുമില്ല.",
        "name": "പേര്",
        "email": "ഇമെയിൽ",
        "login": "ലോഗിൻ",
        "register": "രജിസ്റ്റർ",
        "password": "പാസ്‌വേഡ്",
        "create_account": "അക്കൗണ്ട് സൃഷ്ടിക്കുക"
    },

    "Bengali": {
        **ENGLISH,
        "dashboard": "ড্যাশবোর্ড",
        "companion": "AI সঙ্গী",
        "quiz": "কুইজ",
        "reminders": "রিমাইন্ডার",
        "profile": "প্রোফাইল",
        "logout": "লগ আউট",
        "language": "ভাষা নির্বাচন করুন",
        "menu": "মেনু",
        "welcome": "আপনার দৈনন্দিন যত্ন এখান থেকে শুরু হয়।",
        "send": "পাঠান",
        "message": "আপনার বার্তা লিখুন...",
        "thinking": "Careloop ভাবছে...",
        "generate_quiz": "কুইজ তৈরি করুন",
        "difficulty": "কঠিনতা",
        "easy": "সহজ",
        "medium": "মাঝারি",
        "hard": "কঠিন",
        "reminder": "রিমাইন্ডার",
        "date": "তারিখ",
        "add_reminder": "রিমাইন্ডার যোগ করুন",
        "delete": "মুছুন",
        "no_reminders": "এখনও কোনো রিমাইন্ডার নেই।",
        "name": "নাম",
        "email": "ইমেইল",
        "login": "লগইন",
        "register": "নিবন্ধন",
        "password": "পাসওয়ার্ড",
        "create_account": "অ্যাকাউন্ট তৈরি করুন"
    },

    "Marathi": {
        **ENGLISH,
        "dashboard": "डॅशबोर्ड",
        "companion": "AI साथी",
        "quiz": "प्रश्नमंजुषा",
        "reminders": "स्मरणपत्रे",
        "profile": "प्रोफाइल",
        "logout": "बाहेर पडा",
        "language": "भाषा निवडा",
        "menu": "मेनू",
        "welcome": "तुमची दैनंदिन काळजी इथून सुरू होते.",
        "send": "पाठवा",
        "message": "तुमचा संदेश लिहा...",
        "thinking": "Careloop विचार करत आहे...",
        "generate_quiz": "प्रश्नमंजुषा तयार करा",
        "difficulty": "कठीणपणा",
        "easy": "सोपा",
        "medium": "मध्यम",
        "hard": "कठीण",
        "reminder": "स्मरणपत्र",
        "date": "तारीख",
        "add_reminder": "स्मरणपत्र जोडा",
        "delete": "हटवा",
        "no_reminders": "अद्याप स्मरणपत्रे नाहीत.",
        "name": "नाव",
        "email": "ईमेल",
        "login": "लॉगिन",
        "register": "नोंदणी",
        "password": "पासवर्ड",
        "create_account": "खाते तयार करा"
    },

    "Gujarati": {
        **ENGLISH,
        "dashboard": "ડેશબોર્ડ",
        "companion": "AI સાથી",
        "quiz": "ક્વિઝ",
        "reminders": "રીમાઇન્ડર્સ",
        "profile": "પ્રોફાઇલ",
        "logout": "લૉગ આઉટ",
        "language": "ભાષા પસંદ કરો",
        "menu": "મેનૂ",
        "welcome": "તમારી દૈનિક સંભાળ અહીંથી શરૂ થાય છે.",
        "send": "મોકલો",
        "message": "તમારો સંદેશ લખો...",
        "thinking": "Careloop વિચારી રહ્યું છે...",
        "generate_quiz": "ક્વિઝ બનાવો",
        "difficulty": "કઠિનતા",
        "easy": "સરળ",
        "medium": "મધ્યમ",
        "hard": "અઘરું",
        "reminder": "રિમાઇન્ડર",
        "date": "તારીખ",
        "add_reminder": "રિમાઇન્ડર ઉમેરો",
        "delete": "કાઢી નાખો",
        "name": "નામ",
        "email": "ઇમેઇલ",
        "login": "લૉગિન",
        "register": "નોંધણી",
        "password": "પાસવર્ડ",
        "create_account": "ખાતું બનાવો"
    },

    "Punjabi": {
        **ENGLISH,
        "dashboard": "ਡੈਸ਼ਬੋਰਡ",
        "companion": "AI ਸਾਥੀ",
        "quiz": "ਕੁਇਜ਼",
        "reminders": "ਯਾਦ-ਦਿਹਾਨੀਆਂ",
        "profile": "ਪ੍ਰੋਫ਼ਾਈਲ",
        "logout": "ਲੌਗ ਆਉਟ",
        "language": "ਭਾਸ਼ਾ ਚੁਣੋ",
        "menu": "ਮੀਨੂ",
        "welcome": "ਤੁਹਾਡੀ ਰੋਜ਼ਾਨਾ ਦੇਖਭਾਲ ਇੱਥੋਂ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ।",
        "send": "ਭੇਜੋ",
        "message": "ਆਪਣਾ ਸੁਨੇਹਾ ਲਿਖੋ...",
        "thinking": "Careloop ਸੋਚ ਰਿਹਾ ਹੈ...",
        "generate_quiz": "ਕੁਇਜ਼ ਬਣਾਓ",
        "difficulty": "ਮੁਸ਼ਕਲ",
        "easy": "ਸੌਖਾ",
        "medium": "ਦਰਮਿਆਨਾ",
        "hard": "ਔਖਾ",
        "reminder": "ਯਾਦ-ਦਿਹਾਨੀ",
        "date": "ਤਾਰੀਖ",
        "add_reminder": "ਯਾਦ-ਦਿਹਾਨੀ ਸ਼ਾਮਲ ਕਰੋ",
        "delete": "ਮਿਟਾਓ",
        "name": "ਨਾਮ",
        "email": "ਈਮੇਲ",
        "login": "ਲੌਗਇਨ",
        "register": "ਰਜਿਸਟਰ",
        "password": "ਪਾਸਵਰਡ",
        "create_account": "ਖਾਤਾ ਬਣਾਓ"
    },

    "Arabic": {
        **ENGLISH,
        "dashboard": "لوحة التحكم",
        "companion": "رفيق الذكاء الاصطناعي",
        "quiz": "اختبار سريع",
        "reminders": "التذكيرات",
        "profile": "الملف الشخصي",
        "logout": "تسجيل الخروج",
        "language": "اختر اللغة",
        "menu": "القائمة",
        "welcome": "تبدأ رعايتك اليومية من هنا.",
        "send": "إرسال",
        "message": "اكتب رسالتك...",
        "thinking": "Careloop يفكر...",
        "generate_quiz": "إنشاء اختبار",
        "difficulty": "مستوى الصعوبة",
        "easy": "سهل",
        "medium": "متوسط",
        "hard": "صعب",
        "reminder": "تذكير",
        "date": "التاريخ",
        "add_reminder": "إضافة تذكير",
        "delete": "حذف",
        "name": "الاسم",
        "email": "البريد الإلكتروني",
        "login": "تسجيل الدخول",
        "register": "تسجيل",
        "password": "كلمة المرور",
        "create_account": "إنشاء حساب"
    },

    "French": {
        **ENGLISH,
        "dashboard": "Tableau de bord",
        "companion": "Compagnon IA",
        "quiz": "Quiz rapide",
        "reminders": "Rappels",
        "profile": "Profil",
        "logout": "Déconnexion",
        "language": "Choisir la langue",
        "menu": "Menu",
        "welcome": "Votre bien-être quotidien commence ici.",
        "send": "Envoyer",
        "message": "Écrivez votre message...",
        "thinking": "Careloop réfléchit...",
        "generate_quiz": "Créer un quiz",
        "difficulty": "Difficulté",
        "easy": "Facile",
        "medium": "Moyen",
        "hard": "Difficile",
        "reminder": "Rappel",
        "date": "Date",
        "add_reminder": "Ajouter un rappel",
        "delete": "Supprimer",
        "no_reminders": "Aucun rappel pour le moment.",
        "saved": "Rappel enregistré.",
        "name": "Nom",
        "email": "E-mail",
        "login": "Connexion",
        "register": "Inscription",
        "password": "Mot de passe",
        "create_account": "Créer un compte"
    },

    "Spanish": {
        **ENGLISH,
        "dashboard": "Panel",
        "companion": "Compañero de IA",
        "quiz": "Prueba rápida",
        "reminders": "Recordatorios",
        "profile": "Perfil",
        "logout": "Cerrar sesión",
        "language": "Elegir idioma",
        "menu": "Menú",
        "welcome": "Tu cuidado diario comienza aquí.",
        "send": "Enviar",
        "message": "Escribe tu mensaje...",
        "thinking": "Careloop está pensando...",
        "generate_quiz": "Crear prueba",
        "difficulty": "Dificultad",
        "easy": "Fácil",
        "medium": "Medio",
        "hard": "Difícil",
        "reminder": "Recordatorio",
        "date": "Fecha",
        "add_reminder": "Añadir recordatorio",
        "delete": "Eliminar",
        "no_reminders": "Todavía no hay recordatorios.",
        "saved": "Recordatorio guardado.",
        "name": "Nombre",
        "email": "Correo electrónico",
        "login": "Iniciar sesión",
        "register": "Registrarse",
        "password": "Contraseña",
        "create_account": "Crear cuenta"
    },

    "German": {
        **ENGLISH,
        "dashboard": "Dashboard",
        "companion": "KI-Begleiter",
        "quiz": "Schnellquiz",
        "reminders": "Erinnerungen",
        "profile": "Profil",
        "logout": "Abmelden",
        "language": "Sprache auswählen",
        "menu": "Menü",
        "welcome": "Ihre tägliche Betreuung beginnt hier.",
        "send": "Senden",
        "message": "Nachricht schreiben...",
        "thinking": "Careloop denkt nach...",
        "generate_quiz": "Quiz erstellen",
        "difficulty": "Schwierigkeit",
        "easy": "Einfach",
        "medium": "Mittel",
        "hard": "Schwer",
        "reminder": "Erinnerung",
        "date": "Datum",
        "add_reminder": "Erinnerung hinzufügen",
        "delete": "Löschen",
        "no_reminders": "Noch keine Erinnerungen.",
        "saved": "Erinnerung gespeichert.",
        "name": "Name",
        "email": "E-Mail",
        "login": "Anmelden",
        "register": "Registrieren",
        "password": "Passwort",
        "create_account": "Konto erstellen"
    },

    "Japanese": {
        **ENGLISH,
        "dashboard": "ダッシュボード",
        "companion": "AIコンパニオン",
        "quiz": "クイズ",
        "reminders": "リマインダー",
        "profile": "プロフィール",
        "logout": "ログアウト",
        "language": "言語を選択",
        "menu": "メニュー",
        "welcome": "毎日のケアはここから始まります。",
        "send": "送信",
        "message": "メッセージを入力...",
        "thinking": "Careloopが考えています...",
        "generate_quiz": "クイズを作成",
        "difficulty": "難易度",
        "easy": "簡単",
        "medium": "普通",
        "hard": "難しい",
        "reminder": "リマインダー",
        "date": "日付",
        "add_reminder": "リマインダーを追加",
        "delete": "削除",
        "no_reminders": "リマインダーはまだありません。",
        "saved": "リマインダーを保存しました。",
        "name": "名前",
        "email": "メールアドレス",
        "login": "ログイン",
        "register": "登録",
        "password": "パスワード",
        "create_account": "アカウントを作成"
    }
}


def t(key):
    language = st.session_state.get("language", "English")
    return TRANSLATIONS.get(language, ENGLISH).get(key, ENGLISH.get(key, key))


def selected_ai_language():
    return st.session_state.get("language", "English")


# ==================================================
# DATABASE
# ==================================================

def connection():
    return sqlite3.connect(DB)


def initialize_database():
    with connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT,
                password_hash TEXT,
                salt TEXT
            )
        """)

        columns = {
            row[1] for row in
            conn.execute("PRAGMA table_info(users)").fetchall()
        }

        if "password_hash" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN password_hash TEXT"
            )

        if "salt" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN salt TEXT"
            )

        if "name" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN name TEXT"
            )

        columns = {
            row[1] for row in
            conn.execute("PRAGMA table_info(users)").fetchall()
        }

        if "password" in columns:
            conn.execute("""
                UPDATE users
                SET password_hash = password
                WHERE (password_hash IS NULL OR password_hash = '')
                  AND password IS NOT NULL
            """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                title TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        """)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        180000
    ).hex()


def register(name, email, password):
    email = email.strip().lower()
    salt = secrets.token_hex(16)
    hashed = hash_password(password, salt)

    with connection() as conn:
        columns = {
            row[1] for row in
            conn.execute("PRAGMA table_info(users)").fetchall()
        }

        values = {
            "email": email,
            "name": name.strip(),
            "password_hash": hashed,
            "salt": salt
        }

        if "password" in columns:
            values["password"] = hashed

        if "created_at" in columns:
            values["created_at"] = datetime.now().isoformat()

        insert_columns = [
            col for col in values if col in columns
        ]

        sql = (
            f"INSERT INTO users ({','.join(insert_columns)}) "
            f"VALUES ({','.join(['?'] * len(insert_columns))})"
        )

        conn.execute(
            sql,
            [values[col] for col in insert_columns]
        )


def login(email, password):
    email = email.strip().lower()

    with connection() as conn:
        user = conn.execute("""
            SELECT email, name, password_hash, salt
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    if not user:
        return None

    stored_hash = user[2]
    salt = user[3]

    if not stored_hash or not salt:
        return None

    entered_hash = hash_password(password, salt)

    if secrets.compare_digest(entered_hash, stored_hash):
        return {
            "email": user[0],
            "name": user[1] or "Careloop User"
        }

    return None


# ==================================================
# OPENAI
# ==================================================

def get_client():
    try:
        key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        key = os.getenv("OPENAI_API_KEY", "")

    if not key:
        return None

    return OpenAI(api_key=key)


def ai_reply(client, history):
    language = selected_ai_language()
    name = st.session_state.user["name"]

    instructions = f"""
You are Careloop, an intelligent everyday AI companion.

The user's name is {name}.
Respond in {language}, unless the user asks for another language.

Be conversational, friendly, helpful and honest.
Keep answers easy to understand.
Ask useful follow-up questions when appropriate.

You are an AI, not a human, doctor or therapist.
Never diagnose medical conditions.
For emergencies, recommend contacting local emergency services.
"""

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=instructions,
        input=history
    )

    return response.output_text.strip()


def transcribe(client, recording):
    audio = BytesIO(recording.getvalue())
    audio.name = "recording.wav"

    result = client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio
    )

    return result.text.strip()


def generate_voice(client, text):
    result = client.audio.speech.create(
        model=TTS_MODEL,
        voice="marin",
        input=text[:4000],
        instructions=(
            "Speak naturally and clearly in the language of the text."
        )
    )

    return result.content


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#f7f5ff,#eef2ff,#fff7fb);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#21124b,#49318d);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    padding: 30px;
    border-radius: 24px;
    color: white;
    background: linear-gradient(120deg,#5933ad,#8061df,#a17be8);
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(70,40,150,.15);
}

.hero h1 {
    color: white;
    font-size: 35px;
}

.hero p {
    color: #f4edff;
}

.card {
    background: white;
    border: 1px solid #e8e2f7;
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(50,35,100,.05);
}

.card h3 {
    color: #5737a0;
}

div.stButton > button {
    background: linear-gradient(90deg,#6544c3,#8b69dc);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 650;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# AUTHENTICATION
# ==================================================

def authentication_page():

    st.markdown("""
    <div class="hero">
        <h1>💜 Careloop</h1>
        <p>Your AI companion. Your everyday care.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("## Your everyday companion")
        st.write(
            "Chat, learn, organise your day and get helpful support."
        )
        st.write("🌍 15 languages")
        st.write("🎙️ Voice conversations")
        st.write("🧠 AI-powered quizzes")
        st.write("📅 Personal reminders")

    with right:
        tab1, tab2 = st.tabs([t("login"), t("register")])

        with tab1:
            email = st.text_input(t("email"), key="login_email")
            password = st.text_input(
                t("password"),
                type="password",
                key="login_password"
            )

            if st.button(t("login"), use_container_width=True):
                user = login(email, password)

                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(t("incorrect_login"))

        with tab2:
            name = st.text_input(t("your_name"))
            email = st.text_input(t("email"), key="register_email")
            password = st.text_input(
                t("password") + " (minimum 8 characters)",
                type="password",
                key="register_password"
            )

            if st.button(
                t("create_account"),
                use_container_width=True
            ):
                if not name.strip() or "@" not in email:
                    st.error(t("valid_details"))
                elif len(password) < 8:
                    st.error(t("password_length"))
                else:
                    try:
                        register(name, email, password)
                        st.success(t("account_created"))
                    except sqlite3.IntegrityError:
                        st.error(t("email_exists"))
                    except Exception as error:
                        st.error(f"Registration error: {error}")


# ==================================================
# DASHBOARD
# ==================================================

def dashboard():
    name = st.session_state.user["name"]

    st.markdown(f"""
    <div class="hero">
        <h1>Hello, {name} 👋</h1>
        <p>{t("welcome")}</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown(f"""
        <div class="card">
            <h3>💬 {t("companion")}</h3>
            <p>{t("companion_desc")}</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown(f"""
        <div class="card">
            <h3>🧠 {t("quiz")}</h3>
            <p>{t("quiz_desc")}</p>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown(f"""
        <div class="card">
            <h3>📅 {t("reminders")}</h3>
            <p>{t("reminder_desc")}</p>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# AI COMPANION
# ==================================================

def companion_page(client):
    st.title("💜 " + t("companion"))
    st.caption(t("chat_caption"))

    if "history" not in st.session_state:
        st.session_state.history = []

    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_area(t("message"))
        submitted = st.form_submit_button(t("send"))

    if submitted and prompt.strip():
        st.session_state.history.append({
            "role": "user",
            "content": prompt.strip()
        })

        with st.spinner(t("thinking")):
            try:
                answer = ai_reply(
                    client,
                    st.session_state.history
                )

                st.session_state.history.append({
                    "role": "assistant",
                    "content": answer
                })

                st.session_state.last_reply = answer
                st.session_state.audio_reply = None

            except Exception as error:
                st.error(f"AI error: {error}")

        st.rerun()

    st.divider()
    st.subheader("🎙️ " + t("speak"))
    st.caption(t("microphone_caption"))

    recording = st.audio_input(
        t("record"),
        sample_rate=16000
    )

    if recording is not None:
        if st.button(t("transcribe")):
            with st.spinner(t("listening")):
                try:
                    spoken_text = transcribe(client, recording)

                    if spoken_text:
                        st.session_state.history.append({
                            "role": "user",
                            "content": spoken_text
                        })

                        answer = ai_reply(
                            client,
                            st.session_state.history
                        )

                        st.session_state.history.append({
                            "role": "assistant",
                            "content": answer
                        })

                        st.session_state.last_reply = answer
                        st.session_state.audio_reply = None
                        st.rerun()
                    else:
                        st.warning(t("no_speech"))

                except Exception as error:
                    st.error(f"Voice input error: {error}")

    if st.session_state.get("last_reply"):
        st.divider()
        st.subheader("🔊 " + t("hear"))

        if st.button(t("generate_voice")):
            with st.spinner("Generating voice..."):
                try:
                    st.session_state.audio_reply = generate_voice(
                        client,
                        st.session_state.last_reply
                    )
                except Exception as error:
                    st.error(f"Voice output error: {error}")

        if st.session_state.get("audio_reply"):
            st.audio(
                st.session_state.audio_reply,
                format="audio/mp3"
            )

    if st.button(t("clear_chat")):
        st.session_state.history = []
        st.session_state.last_reply = ""
        st.session_state.audio_reply = None
        st.rerun()


# ==================================================
# QUIZ
# ==================================================

def quiz_page(client):
    st.title("🧠 " + t("quiz"))

    topic = st.text_input(t("topic"))

    difficulty = st.selectbox(
        t("difficulty"),
        [t("easy"), t("medium"), t("hard")]
    )

    if st.button(t("generate_quiz")):
        if not topic.strip():
            st.warning(t("enter_topic"))
        else:
            language = selected_ai_language()

            prompt = f"""
Create 5 multiple-choice questions about {topic}.
Difficulty: {difficulty}.
Language: {language}.

Return only a JSON array.
Each question must contain:
question, options (4 choices), answer (0-3), explanation.
"""

            with st.spinner(t("thinking")):
                try:
                    response = client.responses.create(
                        model=CHAT_MODEL,
                        input=prompt
                    )

                    raw = response.output_text.strip()
                    raw = raw.replace("```json", "").replace("```", "").strip()

                    st.session_state.quiz = json.loads(raw)
                    st.session_state.quiz_topic = topic

                except Exception as error:
                    st.error(f"Quiz error: {error}")

    if st.session_state.get("quiz"):
        st.subheader(st.session_state.quiz_topic)

        with st.form("quiz_answers"):
            answers = []

            for i, question in enumerate(st.session_state.quiz):
                st.write(
                    f"**{i+1}. {question['question']}**"
                )

                answer = st.radio(
                    t("choose_answer"),
                    question["options"],
                    index=None,
                    key=f"answer_{i}"
                )

                answers.append(answer)

            submitted = st.form_submit_button(t("check_answers"))

        if submitted:
            score = 0

            for question, answer in zip(
                st.session_state.quiz,
                answers
            ):
                correct = question["options"][question["answer"]]

                if answer == correct:
                    score += 1
                    st.success(
                        t("correct") + " " + question["explanation"]
                    )
                else:
                    st.error(
                        f"Correct answer: {correct}. "
                        + question["explanation"]
                    )

            st.subheader(
                f"{t('score')}: {score}/{len(st.session_state.quiz)}"
            )


# ==================================================
# REMINDERS
# ==================================================

def reminders_page():
    st.title("📅 " + t("reminders"))

    with st.form("reminder_form", clear_on_submit=True):
        title = st.text_input(t("reminder"))
        due_date = st.date_input(t("date"), value=date.today())

        submitted = st.form_submit_button(t("add_reminder"))

    if submitted:
        if title.strip():
            with connection() as conn:
                conn.execute("""
                    INSERT INTO reminders(email,title,due_date)
                    VALUES(?,?,?)
                """, (
                    st.session_state.user["email"],
                    title.strip(),
                    due_date.isoformat()
                ))

            st.success(t("saved"))
        else:
            st.warning(t("reminder"))

    with connection() as conn:
        reminders = conn.execute("""
            SELECT id,title,due_date
            FROM reminders
            WHERE email=?
            ORDER BY due_date
        """, (
            st.session_state.user["email"],
        )).fetchall()

    if not reminders:
        st.info(t("no_reminders"))

    for rid, title, due in reminders:
        col1, col2 = st.columns([5, 1])

        col1.write(f"**{title}** — {due}")

        if col2.button(t("delete"), key=f"delete_{rid}"):
            with connection() as conn:
                conn.execute(
                    "DELETE FROM reminders WHERE id=? AND email=?",
                    (rid, st.session_state.user["email"])
                )

            st.rerun()


# ==================================================
# PROFILE
# ==================================================

def profile_page():
    st.title("👤 " + t("profile"))

    st.subheader(t("profile_info"))
    st.write(t("name") + ":", st.session_state.user["name"])
    st.write(t("email") + ":", st.session_state.user["email"])

    st.info(
        "Change your language using the language selector "
        "in the sidebar."
    )


# ==================================================
# MAIN APPLICATION
# ==================================================



def main():
    initialize_database()

    if "language" not in st.session_state:
        st.session_state.language = "English"

    if "user" not in st.session_state:
        st.session_state.user = {
            "name": "Guest",
            "email": "guest@careloop.local"
        }

    if "history" not in st.session_state:
        st.session_state.history = []

    if "last_reply" not in st.session_state:
        st.session_state.last_reply = ""

    if "audio_reply" not in st.session_state:
        st.session_state.audio_reply = None

    client = get_client()

    if not client:
        st.error(t("api_missing"))
        return

    with st.sidebar:
        st.title("💜 Careloop")
        st.write("Hello, Guest 👋")

        language_options = list(LANGUAGES.keys())

        # Convert the saved language into its display label.
        current_language = st.session_state.language

        current_label = next(
            (
                label
                for label, language_name in LANGUAGES.items()
                if language_name == current_language
            ),
            "English"
        )

        selected_label = st.selectbox(
            t("language"),
            language_options,
            index=language_options.index(current_label),
            key="main_language_selector"
        )

        # Store the canonical language name, not the display label.
        if selected_label != current_label:
            st.session_state.language = LANGUAGES[selected_label]
            st.rerun()

        st.divider()

        page = st.radio(
            t("menu"),
            [
                t("dashboard"),
                t("companion"),
                t("quiz"),
                t("reminders"),
                t("profile")
            ]
        )

    if page == t("dashboard"):
        dashboard()

    elif page == t("companion"):
        companion_page(client)

    elif page == t("quiz"):
        quiz_page(client)

    elif page == t("reminders"):
        reminders_page()

    elif page == t("profile"):
        profile_page()


if __name__ == "__main__":
    main()
