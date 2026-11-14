
import streamlit as st
from openai import OpenAI
from datetime import date, time

# =========================================================
# CARELOOP CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Careloop",
    page_icon="💙",
    layout="centered"
)

MODEL = "gpt-6-luna"

# =========================================================
# TRANSLATIONS
# =========================================================

TRANSLATIONS = {
    "English": {
        "welcome": "Welcome to Careloop!",
        "tagline": "Your AI companion. Your everyday care.",
        "name": "Your name",
        "phone": "Mobile number",
        "continue": "Continue",
        "verify": "Verify and Login",
        "otp_title": "Verify your mobile number",
        "otp_prompt": "Enter your OTP",
        "demo_otp": "Demo OTP: 123456",
        "invalid_name": "Please enter your name.",
        "invalid_phone": "Enter a valid 10-digit mobile number.",
        "wrong_otp": "Incorrect OTP. Try again.",
        "home": "Home",
        "ai": "AI Companion",
        "quiz": "Quizzes",
        "reminders": "Reminders",
        "languages": "Languages",
        "profile": "Profile",
        "logout": "Logout",
        "hello": "Hello",
        "what_do": "What would you like to do today?",
        "open_ai": "Open AI Companion",
        "start_quiz": "Start a Quiz",
        "view_reminders": "View Reminders",
        "chat_title": "Talk to Careloop",
        "choose_language": "Choose your language",
        "message": "Message Careloop...",
        "thinking": "Careloop is thinking...",
        "clear_chat": "Clear conversation",
        "quiz_title": "Test your knowledge!",
        "submit_quiz": "Submit Quiz",
        "your_score": "Your Score",
        "excellent": "Excellent! Perfect score!",
        "great": "Great work! Keep practising!",
        "improve": "Good attempt! Keep learning!",
        "try_again": "Try Again",
        "question": "Question",
        "correct": "Correct answer",
        "all_questions": "Please answer all questions.",
        "add_reminder": "Add a reminder",
        "reminder": "Reminder",
        "reminder_date": "Date",
        "reminder_time": "Time",
        "save_reminder": "Save Reminder",
        "added": "Reminder added!",
        "empty_reminder": "You have no reminders yet.",
        "delete": "Delete",
        "reminder_list": "Your Reminder List",
        "language_title": "Choose Your Language",
        "save_language": "Save Language",
        "language_saved": "Language saved!",
        "profile_title": "My Profile",
        "account_details": "Your account details",
        "preferred": "Preferred language",
        "logged_in": "Login successful!",
        "api_error": "Unable to get an AI response. Check your API billing and connection.",
        "api_missing": "API key not configured.",
        "quiz_intro": "Answer these three questions.",
        "login_back": "Back",
        "settings": "Settings",
        "assistant_description": "Talk with your AI companion.",
        "quiz_description": "Challenge yourself with a quick quiz.",
        "reminder_description": "Keep track of important things.",
        "language_description": "Choose your preferred language.",
        "no_chat": "Start a conversation with Careloop!",
        "question_1": "Which planet is known as the Red Planet?",
        "question_2": "How many days are there in a leap year?",
        "question_3": "Which is the largest ocean?",
        "option_earth": "Earth",
        "option_mars": "Mars",
        "option_jupiter": "Jupiter",
        "option_venus": "Venus",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "Indian Ocean",
        "option_atlantic": "Atlantic Ocean",
        "option_pacific": "Pacific Ocean",
        "option_arctic": "Arctic Ocean",
        "quiz_results": "Your Quiz Results",
        "saved": "Saved successfully!",
        "select_answer": "Choose your answer",
        "quiz_zero": "Keep learning! You can try again.",
        "reminder_empty": "Please enter a reminder.",
        "logout_confirm": "You have logged out."
    },

    "Kannada": {
        "welcome": "Careloop ಗೆ ಸ್ವಾಗತ!",
        "tagline": "ನಿಮ್ಮ AI ಸಂಗಾತಿ. ನಿಮ್ಮ ದೈನಂದಿನ ಆರೈಕೆ.",
        "name": "ನಿಮ್ಮ ಹೆಸರು",
        "phone": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        "continue": "ಮುಂದುವರಿಸಿ",
        "verify": "ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಲಾಗಿನ್ ಮಾಡಿ",
        "otp_title": "ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ಪರಿಶೀಲಿಸಿ",
        "otp_prompt": "OTP ನಮೂದಿಸಿ",
        "demo_otp": "ಡೆಮೋ OTP: 123456",
        "invalid_name": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "invalid_phone": "ಸರಿಯಾದ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "wrong_otp": "ತಪ್ಪಾದ OTP. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "home": "ಮುಖಪುಟ",
        "ai": "AI ಸಹಾಯಕ",
        "quiz": "ರಸಪ್ರಶ್ನೆಗಳು",
        "reminders": "ಜ್ಞಾಪನೆಗಳು",
        "languages": "ಭಾಷೆಗಳು",
        "profile": "ಪ್ರೊಫೈಲ್",
        "logout": "ಲಾಗ್ ಔಟ್",
        "hello": "ನಮಸ್ಕಾರ",
        "what_do": "ಇಂದು ನೀವು ಏನು ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?",
        "open_ai": "AI ಸಹಾಯಕ ತೆರೆಯಿರಿ",
        "start_quiz": "ರಸಪ್ರಶ್ನೆ ಪ್ರಾರಂಭಿಸಿ",
        "view_reminders": "ಜ್ಞಾಪನೆಗಳನ್ನು ನೋಡಿ",
        "chat_title": "Careloop ಜೊತೆ ಮಾತನಾಡಿ",
        "choose_language": "ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "message": "Careloop ಗೆ ಸಂದೇಶ ಕಳುಹಿಸಿ...",
        "thinking": "Careloop ಯೋಚಿಸುತ್ತಿದೆ...",
        "clear_chat": "ಸಂಭಾಷಣೆ ಅಳಿಸಿ",
        "quiz_title": "ನಿಮ್ಮ ಜ್ಞಾನವನ್ನು ಪರೀಕ್ಷಿಸಿ!",
        "submit_quiz": "ರಸಪ್ರಶ್ನೆ ಸಲ್ಲಿಸಿ",
        "your_score": "ನಿಮ್ಮ ಅಂಕಗಳು",
        "excellent": "ಅದ್ಭುತ! ಪೂರ್ಣ ಅಂಕಗಳು!",
        "great": "ಚೆನ್ನಾಗಿದೆ! ಅಭ್ಯಾಸ ಮುಂದುವರಿಸಿ!",
        "improve": "ಒಳ್ಳೆಯ ಪ್ರಯತ್ನ! ಕಲಿಯುತ್ತಿರಿ!",
        "try_again": "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ",
        "question": "ಪ್ರಶ್ನೆ",
        "correct": "ಸರಿಯಾದ ಉತ್ತರ",
        "all_questions": "ಎಲ್ಲಾ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ.",
        "add_reminder": "ಜ್ಞಾಪನೆ ಸೇರಿಸಿ",
        "reminder": "ಜ್ಞಾಪನೆ",
        "reminder_date": "ದಿನಾಂಕ",
        "reminder_time": "ಸಮಯ",
        "save_reminder": "ಜ್ಞಾಪನೆ ಉಳಿಸಿ",
        "added": "ಜ್ಞಾಪನೆ ಸೇರಿಸಲಾಗಿದೆ!",
        "empty_reminder": "ಇನ್ನೂ ಯಾವುದೇ ಜ್ಞಾಪನೆಗಳಿಲ್ಲ.",
        "delete": "ಅಳಿಸಿ",
        "reminder_list": "ನಿಮ್ಮ ಜ್ಞಾಪನೆಗಳ ಪಟ್ಟಿ",
        "language_title": "ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "save_language": "ಭಾಷೆ ಉಳಿಸಿ",
        "language_saved": "ಭಾಷೆ ಉಳಿಸಲಾಗಿದೆ!",
        "profile_title": "ನನ್ನ ಪ್ರೊಫೈಲ್",
        "account_details": "ನಿಮ್ಮ ಖಾತೆಯ ವಿವರಗಳು",
        "preferred": "ಆದ್ಯತೆಯ ಭಾಷೆ",
        "logged_in": "ಲಾಗಿನ್ ಯಶಸ್ವಿಯಾಗಿದೆ!",
        "api_error": "AI ಉತ್ತರ ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. API ಬಿಲ್ಲಿಂಗ್ ಪರಿಶೀಲಿಸಿ.",
        "api_missing": "API ಕೀ ಹೊಂದಿಸಲಾಗಿಲ್ಲ.",
        "quiz_intro": "ಈ ಮೂರು ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ.",
        "login_back": "ಹಿಂದೆ",
        "settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "assistant_description": "ನಿಮ್ಮ AI ಸಂಗಾತಿಯೊಂದಿಗೆ ಮಾತನಾಡಿ.",
        "quiz_description": "ಸಣ್ಣ ರಸಪ್ರಶ್ನೆಯೊಂದಿಗೆ ನಿಮ್ಮ ಜ್ಞಾನ ಪರೀಕ್ಷಿಸಿ.",
        "reminder_description": "ಮುಖ್ಯ ವಿಷಯಗಳನ್ನು ನೆನಪಿಡಿ.",
        "language_description": "ನಿಮ್ಮ ಆದ್ಯತೆಯ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "no_chat": "Careloop ಜೊತೆ ಸಂಭಾಷಣೆ ಪ್ರಾರಂಭಿಸಿ!",
        "question_1": "ಕೆಂಪು ಗ್ರಹ ಎಂದು ಯಾವ ಗ್ರಹವನ್ನು ಕರೆಯುತ್ತಾರೆ?",
        "question_2": "ಅಧಿಕ ವರ್ಷದ ದಿನಗಳು ಎಷ್ಟು?",
        "question_3": "ವಿಶ್ವದ ಅತಿ ದೊಡ್ಡ ಸಾಗರ ಯಾವುದು?",
        "option_earth": "ಭೂಮಿ",
        "option_mars": "ಮಂಗಳ",
        "option_jupiter": "ಗುರು",
        "option_venus": "ಶುಕ್ರ",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "ಹಿಂದೂ ಮಹಾಸಾಗರ",
        "option_atlantic": "ಅಟ್ಲಾಂಟಿಕ್ ಮಹಾಸಾಗರ",
        "option_pacific": "ಪೆಸಿಫಿಕ್ ಮಹಾಸಾಗರ",
        "option_arctic": "ಆರ್ಕ್ಟಿಕ್ ಮಹಾಸಾಗರ",
        "quiz_results": "ನಿಮ್ಮ ರಸಪ್ರಶ್ನೆ ಫಲಿತಾಂಶ",
        "saved": "ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!",
        "select_answer": "ಉತ್ತರ ಆಯ್ಕೆಮಾಡಿ",
        "quiz_zero": "ಕಲಿಯುತ್ತಿರಿ! ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "reminder_empty": "ದಯವಿಟ್ಟು ಜ್ಞಾಪನೆಯನ್ನು ನಮೂದಿಸಿ.",
        "logout_confirm": "ನೀವು ಲಾಗ್ ಔಟ್ ಆಗಿದ್ದೀರಿ."
    },

    "Hindi": {
        "welcome": "Careloop में आपका स्वागत है!",
        "tagline": "आपका AI साथी। आपकी रोज़मर्रा की देखभाल।",
        "name": "आपका नाम",
        "phone": "मोबाइल नंबर",
        "continue": "जारी रखें",
        "verify": "सत्यापित करें और लॉगिन करें",
        "otp_title": "अपना मोबाइल नंबर सत्यापित करें",
        "otp_prompt": "OTP दर्ज करें",
        "demo_otp": "डेमो OTP: 123456",
        "invalid_name": "कृपया अपना नाम दर्ज करें।",
        "invalid_phone": "10 अंकों का सही मोबाइल नंबर दर्ज करें।",
        "wrong_otp": "गलत OTP। फिर से प्रयास करें।",
        "home": "होम",
        "ai": "AI साथी",
        "quiz": "प्रश्नोत्तरी",
        "reminders": "रिमाइंडर",
        "languages": "भाषाएँ",
        "profile": "प्रोफ़ाइल",
        "logout": "लॉग आउट",
        "hello": "नमस्ते",
        "what_do": "आज आप क्या करना चाहेंगे?",
        "open_ai": "AI साथी खोलें",
        "start_quiz": "प्रश्नोत्तरी शुरू करें",
        "view_reminders": "रिमाइंडर देखें",
        "chat_title": "Careloop से बात करें",
        "choose_language": "अपनी भाषा चुनें",
        "message": "Careloop को संदेश भेजें...",
        "thinking": "Careloop सोच रहा है...",
        "clear_chat": "बातचीत मिटाएँ",
        "quiz_title": "अपने ज्ञान की जाँच करें!",
        "submit_quiz": "प्रश्नोत्तरी जमा करें",
        "your_score": "आपके अंक",
        "excellent": "शानदार! पूरे अंक!",
        "great": "बहुत अच्छा! अभ्यास जारी रखें!",
        "improve": "अच्छा प्रयास! सीखते रहें!",
        "try_again": "फिर से प्रयास करें",
        "question": "प्रश्न",
        "correct": "सही उत्तर",
        "all_questions": "कृपया सभी प्रश्नों के उत्तर दें।",
        "add_reminder": "रिमाइंडर जोड़ें",
        "reminder": "रिमाइंडर",
        "reminder_date": "तारीख",
        "reminder_time": "समय",
        "save_reminder": "रिमाइंडर सहेजें",
        "added": "रिमाइंडर जोड़ दिया गया!",
        "empty_reminder": "अभी कोई रिमाइंडर नहीं है।",
        "delete": "हटाएँ",
        "reminder_list": "आपकी रिमाइंडर सूची",
        "language_title": "अपनी भाषा चुनें",
        "save_language": "भाषा सहेजें",
        "language_saved": "भाषा सहेजी गई!",
        "profile_title": "मेरी प्रोफ़ाइल",
        "account_details": "आपके खाते का विवरण",
        "preferred": "पसंदीदा भाषा",
        "logged_in": "लॉगिन सफल!",
        "api_error": "AI उत्तर नहीं मिल सका। API बिलिंग जाँचें।",
        "api_missing": "API कुंजी सेट नहीं है।",
        "quiz_intro": "इन तीन प्रश्नों के उत्तर दें।",
        "login_back": "वापस",
        "settings": "सेटिंग्स",
        "assistant_description": "अपने AI साथी से बात करें।",
        "quiz_description": "एक छोटी प्रश्नोत्तरी खेलें।",
        "reminder_description": "महत्वपूर्ण बातें याद रखें।",
        "language_description": "अपनी पसंदीदा भाषा चुनें।",
        "no_chat": "Careloop से बातचीत शुरू करें!",
        "question_1": "किस ग्रह को लाल ग्रह कहा जाता है?",
        "question_2": "लीप वर्ष में कितने दिन होते हैं?",
        "question_3": "विश्व का सबसे बड़ा महासागर कौन सा है?",
        "option_earth": "पृथ्वी",
        "option_mars": "मंगल",
        "option_jupiter": "बृहस्पति",
        "option_venus": "शुक्र",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "हिंद महासागर",
        "option_atlantic": "अटलांटिक महासागर",
        "option_pacific": "प्रशांत महासागर",
        "option_arctic": "आर्कटिक महासागर",
        "quiz_results": "आपका परिणाम",
        "saved": "सफलतापूर्वक सहेजा गया!",
        "select_answer": "अपना उत्तर चुनें",
        "quiz_zero": "सीखते रहें! फिर प्रयास करें।",
        "reminder_empty": "कृपया रिमाइंडर लिखें।",
        "logout_confirm": "आप लॉग आउट हो गए हैं।"
    },

    "Tamil": {
        "welcome": "Careloop-க்கு வரவேற்கிறோம்!",
        "tagline": "உங்கள் AI துணைவர். உங்கள் அன்றாட பராமரிப்பு.",
        "name": "உங்கள் பெயர்",
        "phone": "கைபேசி எண்",
        "continue": "தொடரவும்",
        "verify": "சரிபார்த்து உள்நுழையவும்",
        "otp_title": "உங்கள் கைபேசி எண்ணை சரிபார்க்கவும்",
        "otp_prompt": "OTP உள்ளிடவும்",
        "demo_otp": "டெமோ OTP: 123456",
        "invalid_name": "உங்கள் பெயரை உள்ளிடவும்.",
        "invalid_phone": "சரியான 10 இலக்க எண்ணை உள்ளிடவும்.",
        "wrong_otp": "தவறான OTP. மீண்டும் முயற்சிக்கவும்.",
        "home": "முகப்பு",
        "ai": "AI துணைவர்",
        "quiz": "வினாடி வினா",
        "reminders": "நினைவூட்டல்கள்",
        "languages": "மொழிகள்",
        "profile": "சுயவிவரம்",
        "logout": "வெளியேறு",
        "hello": "வணக்கம்",
        "what_do": "இன்று நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?",
        "open_ai": "AI துணைவரை திறக்கவும்",
        "start_quiz": "வினாடி வினாவை தொடங்கவும்",
        "view_reminders": "நினைவூட்டல்களை பார்க்கவும்",
        "chat_title": "Careloop உடன் பேசுங்கள்",
        "choose_language": "உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
        "message": "Careloop-க்கு செய்தி அனுப்பவும்...",
        "thinking": "Careloop யோசிக்கிறது...",
        "clear_chat": "உரையாடலை அழிக்கவும்",
        "quiz_title": "உங்கள் அறிவை சோதிக்கவும்!",
        "submit_quiz": "வினாடி வினாவை சமர்ப்பிக்கவும்",
        "your_score": "உங்கள் மதிப்பெண்",
        "excellent": "அருமை! முழு மதிப்பெண்கள்!",
        "great": "நன்றாக செய்தீர்கள்!",
        "improve": "நல்ல முயற்சி! தொடர்ந்து கற்றுக்கொள்ளுங்கள்!",
        "try_again": "மீண்டும் முயற்சிக்கவும்",
        "question": "கேள்வி",
        "correct": "சரியான பதில்",
        "all_questions": "அனைத்து கேள்விகளுக்கும் பதிலளிக்கவும்.",
        "add_reminder": "நினைவூட்டலை சேர்க்கவும்",
        "reminder": "நினைவூட்டல்",
        "reminder_date": "தேதி",
        "reminder_time": "நேரம்",
        "save_reminder": "சேமிக்கவும்",
        "added": "நினைவூட்டல் சேர்க்கப்பட்டது!",
        "empty_reminder": "நினைவூட்டல்கள் எதுவும் இல்லை.",
        "delete": "நீக்கவும்",
        "reminder_list": "உங்கள் நினைவூட்டல்கள்",
        "language_title": "உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
        "save_language": "மொழியை சேமிக்கவும்",
        "language_saved": "மொழி சேமிக்கப்பட்டது!",
        "profile_title": "என் சுயவிவரம்",
        "account_details": "உங்கள் கணக்கு விவரங்கள்",
        "preferred": "விருப்பமான மொழி",
        "logged_in": "உள்நுழைவு வெற்றிகரமானது!",
        "api_error": "AI பதிலைப் பெற முடியவில்லை. API கட்டணத்தை சரிபார்க்கவும்.",
        "api_missing": "API விசை அமைக்கப்படவில்லை.",
        "quiz_intro": "இந்த மூன்று கேள்விகளுக்கும் பதிலளிக்கவும்.",
        "login_back": "பின்னால்",
        "settings": "அமைப்புகள்",
        "assistant_description": "உங்கள் AI துணைவருடன் பேசுங்கள்.",
        "quiz_description": "சிறிய வினாடி வினாவில் பங்கேற்கவும்.",
        "reminder_description": "முக்கியமானவற்றை நினைவில் வைக்கவும்.",
        "language_description": "உங்கள் விருப்பமான மொழியை தேர்ந்தெடுக்கவும்.",
        "no_chat": "Careloop உடன் உரையாடலை தொடங்குங்கள்!",
        "question_1": "சிவப்பு கிரகம் என்று அழைக்கப்படுவது எது?",
        "question_2": "ஒரு லீப் ஆண்டில் எத்தனை நாட்கள்?",
        "question_3": "உலகின் மிகப்பெரிய பெருங்கடல் எது?",
        "option_earth": "பூமி",
        "option_mars": "செவ்வாய்",
        "option_jupiter": "வியாழன்",
        "option_venus": "வெள்ளி",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "இந்தியப் பெருங்கடல்",
        "option_atlantic": "அட்லாண்டிக் பெருங்கடல்",
        "option_pacific": "பசிபிக் பெருங்கடல்",
        "option_arctic": "ஆர்க்டிக் பெருங்கடல்",
        "quiz_results": "உங்கள் வினாடி வினா முடிவுகள்",
        "saved": "வெற்றிகரமாக சேமிக்கப்பட்டது!",
        "select_answer": "பதிலை தேர்ந்தெடுக்கவும்",
        "quiz_zero": "தொடர்ந்து கற்றுக்கொள்ளுங்கள்!",
        "reminder_empty": "நினைவூட்டலை உள்ளிடவும்.",
        "logout_confirm": "நீங்கள் வெளியேறிவிட்டீர்கள்."
    },

    "Telugu": {
        "welcome": "Careloop కు స్వాగతం!",
        "tagline": "మీ AI సహచరుడు. మీ రోజువారీ సంరక్షణ.",
        "name": "మీ పేరు",
        "phone": "మొబైల్ నంబర్",
        "continue": "కొనసాగించండి",
        "verify": "ధృవీకరించి లాగిన్ చేయండి",
        "otp_title": "మీ మొబైల్ నంబర్‌ను ధృవీకరించండి",
        "otp_prompt": "OTP నమోదు చేయండి",
        "demo_otp": "డెమో OTP: 123456",
        "invalid_name": "దయచేసి మీ పేరు నమోదు చేయండి.",
        "invalid_phone": "సరైన 10 అంకెల నంబర్ నమోదు చేయండి.",
        "wrong_otp": "తప్పు OTP. మళ్లీ ప్రయత్నించండి.",
        "home": "హోమ్",
        "ai": "AI సహచరుడు",
        "quiz": "క్విజ్‌లు",
        "reminders": "రిమైండర్‌లు",
        "languages": "భాషలు",
        "profile": "ప్రొఫైల్",
        "logout": "లాగ్ అవుట్",
        "hello": "నమస్కారం",
        "what_do": "ఈరోజు మీరు ఏమి చేయాలనుకుంటున్నారు?",
        "open_ai": "AI సహచరుడిని తెరవండి",
        "start_quiz": "క్విజ్ ప్రారంభించండి",
        "view_reminders": "రిమైండర్‌లను చూడండి",
        "chat_title": "Careloop తో మాట్లాడండి",
        "choose_language": "మీ భాషను ఎంచుకోండి",
        "message": "Careloop కు సందేశం పంపండి...",
        "thinking": "Careloop ఆలోచిస్తోంది...",
        "clear_chat": "సంభాషణను తొలగించండి",
        "quiz_title": "మీ జ్ఞానాన్ని పరీక్షించుకోండి!",
        "submit_quiz": "క్విజ్ సమర్పించండి",
        "your_score": "మీ స్కోర్",
        "excellent": "అద్భుతం! పూర్తి మార్కులు!",
        "great": "చాలా బాగా చేశారు!",
        "improve": "మంచి ప్రయత్నం! నేర్చుకుంటూ ఉండండి!",
        "try_again": "మళ్లీ ప్రయత్నించండి",
        "question": "ప్రశ్న",
        "correct": "సరైన సమాధానం",
        "all_questions": "అన్ని ప్రశ్నలకు సమాధానం ఇవ్వండి.",
        "add_reminder": "రిమైండర్ జోడించండి",
        "reminder": "రిమైండర్",
        "reminder_date": "తేదీ",
        "reminder_time": "సమయం",
        "save_reminder": "రిమైండర్ సేవ్ చేయండి",
        "added": "రిమైండర్ జోడించబడింది!",
        "empty_reminder": "రిమైండర్‌లు లేవు.",
        "delete": "తొలగించండి",
        "reminder_list": "మీ రిమైండర్‌లు",
        "language_title": "మీ భాషను ఎంచుకోండి",
        "save_language": "భాషను సేవ్ చేయండి",
        "language_saved": "భాష సేవ్ చేయబడింది!",
        "profile_title": "నా ప్రొఫైల్",
        "account_details": "మీ ఖాతా వివరాలు",
        "preferred": "ఇష్టమైన భాష",
        "logged_in": "లాగిన్ విజయవంతమైంది!",
        "api_error": "AI సమాధానం పొందలేకపోయాం. API బిల్లింగ్ తనిఖీ చేయండి.",
        "api_missing": "API కీ సెట్ చేయబడలేదు.",
        "quiz_intro": "ఈ మూడు ప్రశ్నలకు సమాధానం ఇవ్వండి.",
        "login_back": "వెనక్కి",
        "settings": "సెట్టింగ్‌లు",
        "assistant_description": "మీ AI సహచరుడితో మాట్లాడండి.",
        "quiz_description": "చిన్న క్విజ్‌లో పాల్గొనండి.",
        "reminder_description": "ముఖ్యమైన విషయాలను గుర్తుంచుకోండి.",
        "language_description": "మీకు నచ్చిన భాషను ఎంచుకోండి.",
        "no_chat": "Careloop తో సంభాషణ ప్రారంభించండి!",
        "question_1": "ఎర్ర గ్రహం అని ఏ గ్రహాన్ని పిలుస్తారు?",
        "question_2": "లీపు సంవత్సరంలో ఎన్ని రోజులు ఉంటాయి?",
        "question_3": "ప్రపంచంలో అతిపెద్ద సముద్రం ఏది?",
        "option_earth": "భూమి",
        "option_mars": "అంగారకుడు",
        "option_jupiter": "బృహస్పతి",
        "option_venus": "శుక్రుడు",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "హిందూ మహాసముద్రం",
        "option_atlantic": "అట్లాంటిక్ మహాసముద్రం",
        "option_pacific": "పసిఫిక్ మహాసముద్రం",
        "option_arctic": "ఆర్కిటిక్ మహాసముద్రం",
        "quiz_results": "మీ క్విజ్ ఫలితాలు",
        "saved": "విజయవంతంగా సేవ్ చేయబడింది!",
        "select_answer": "సమాధానం ఎంచుకోండి",
        "quiz_zero": "నేర్చుకుంటూ ఉండండి! మళ్లీ ప్రయత్నించండి.",
        "reminder_empty": "దయచేసి రిమైండర్ నమోదు చేయండి.",
        "logout_confirm": "మీరు లాగ్ అవుట్ అయ్యారు."
    },

    "Malayalam": {
        "welcome": "Careloop-ലേക്ക് സ്വാഗതം!",
        "tagline": "നിങ്ങളുടെ AI കൂട്ടുകാരൻ. നിങ്ങളുടെ ദൈനംദിന പരിചരണം.",
        "name": "നിങ്ങളുടെ പേര്",
        "phone": "മൊബൈൽ നമ്പർ",
        "continue": "തുടരുക",
        "verify": "പരിശോധിച്ച് ലോഗിൻ ചെയ്യുക",
        "otp_title": "മൊബൈൽ നമ്പർ പരിശോധിക്കുക",
        "otp_prompt": "OTP നൽകുക",
        "demo_otp": "ഡെമോ OTP: 123456",
        "invalid_name": "ദയവായി പേര് നൽകുക.",
        "invalid_phone": "ശരിയായ 10 അക്ക നമ്പർ നൽകുക.",
        "wrong_otp": "തെറ്റായ OTP. വീണ്ടും ശ്രമിക്കുക.",
        "home": "ഹോം",
        "ai": "AI കൂട്ടുകാരൻ",
        "quiz": "ക്വിസ്",
        "reminders": "ഓർമ്മപ്പെടുത്തലുകൾ",
        "languages": "ഭാഷകൾ",
        "profile": "പ്രൊഫൈൽ",
        "logout": "ലോഗ് ഔട്ട്",
        "hello": "നമസ്കാരം",
        "what_do": "ഇന്ന് നിങ്ങൾ എന്താണ് ചെയ്യാൻ ആഗ്രഹിക്കുന്നത്?",
        "open_ai": "AI കൂട്ടുകാരനെ തുറക്കുക",
        "start_quiz": "ക്വിസ് ആരംഭിക്കുക",
        "view_reminders": "ഓർമ്മപ്പെടുത്തലുകൾ കാണുക",
        "chat_title": "Careloop-നോട് സംസാരിക്കുക",
        "choose_language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "message": "Careloop-ന് സന്ദേശം അയയ്ക്കുക...",
        "thinking": "Careloop ചിന്തിക്കുന്നു...",
        "clear_chat": "സംഭാഷണം മായ്ക്കുക",
        "quiz_title": "നിങ്ങളുടെ അറിവ് പരിശോധിക്കുക!",
        "submit_quiz": "ക്വിസ് സമർപ്പിക്കുക",
        "your_score": "നിങ്ങളുടെ സ്കോർ",
        "excellent": "മികച്ചത്! മുഴുവൻ മാർക്കും!",
        "great": "നന്നായി ചെയ്തു!",
        "improve": "നല്ല ശ്രമം! പഠനം തുടരുക!",
        "try_again": "വീണ്ടും ശ്രമിക്കുക",
        "question": "ചോദ്യം",
        "correct": "ശരിയായ ഉത്തരം",
        "all_questions": "എല്ലാ ചോദ്യങ്ങൾക്കും ഉത്തരം നൽകുക.",
        "add_reminder": "ഓർമ്മപ്പെടുത്തൽ ചേർക്കുക",
        "reminder": "ഓർമ്മപ്പെടുത്തൽ",
        "reminder_date": "തീയതി",
        "reminder_time": "സമയം",
        "save_reminder": "സേവ് ചെയ്യുക",
        "added": "ഓർമ്മപ്പെടുത്തൽ ചേർത്തു!",
        "empty_reminder": "ഓർമ്മപ്പെടുത്തലുകൾ ഒന്നുമില്ല.",
        "delete": "ഇല്ലാതാക്കുക",
        "reminder_list": "നിങ്ങളുടെ ഓർമ്മപ്പെടുത്തലുകൾ",
        "language_title": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "save_language": "ഭാഷ സേവ് ചെയ്യുക",
        "language_saved": "ഭാഷ സേവ് ചെയ്തു!",
        "profile_title": "എന്റെ പ്രൊഫൈൽ",
        "account_details": "അക്കൗണ്ട് വിവരങ്ങൾ",
        "preferred": "ഇഷ്ടപ്പെട്ട ഭാഷ",
        "logged_in": "ലോഗിൻ വിജയിച്ചു!",
        "api_error": "AI മറുപടി ലഭിച്ചില്ല. API ബില്ലിംഗ് പരിശോധിക്കുക.",
        "api_missing": "API കീ ക്രമീകരിച്ചിട്ടില്ല.",
        "quiz_intro": "ഈ മൂന്ന് ചോദ്യങ്ങൾക്ക് ഉത്തരം നൽകുക.",
        "login_back": "തിരികെ",
        "settings": "ക്രമീകരണങ്ങൾ",
        "assistant_description": "നിങ്ങളുടെ AI കൂട്ടുകാരനോട് സംസാരിക്കുക.",
        "quiz_description": "ഒരു ചെറിയ ക്വിസ് കളിക്കുക.",
        "reminder_description": "പ്രധാന കാര്യങ്ങൾ ഓർമ്മിക്കുക.",
        "language_description": "ഇഷ്ടപ്പെട്ട ഭാഷ തിരഞ്ഞെടുക്കുക.",
        "no_chat": "Careloop-നൊപ്പം സംഭാഷണം ആരംഭിക്കുക!",
        "question_1": "ചുവന്ന ഗ്രഹം എന്നറിയപ്പെടുന്നത് ഏത്?",
        "question_2": "ഒരു അധിവർഷത്തിൽ എത്ര ദിവസങ്ങളുണ്ട്?",
        "question_3": "ലോകത്തിലെ ഏറ്റവും വലിയ സമുദ്രം ഏതാണ്?",
        "option_earth": "ഭൂമി",
        "option_mars": "ചൊവ്വ",
        "option_jupiter": "വ്യാഴം",
        "option_venus": "ശുക്രൻ",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "ഇന്ത്യൻ മഹാസമുദ്രം",
        "option_atlantic": "അറ്റ്ലാന്റിക് സമുദ്രം",
        "option_pacific": "പസഫിക് സമുദ്രം",
        "option_arctic": "ആർട്ടിക് സമുദ്രം",
        "quiz_results": "നിങ്ങളുടെ ക്വിസ് ഫലം",
        "saved": "വിജയകരമായി സേവ് ചെയ്തു!",
        "select_answer": "ഉത്തരം തിരഞ്ഞെടുക്കുക",
        "quiz_zero": "പഠനം തുടരുക! വീണ്ടും ശ്രമിക്കുക.",
        "reminder_empty": "ഓർമ്മപ്പെടുത്തൽ നൽകുക.",
        "logout_confirm": "നിങ്ങൾ ലോഗ് ഔട്ട് ചെയ്തു."
    },

    "Bengali": {
        "welcome": "Careloop-এ স্বাগতম!",
        "tagline": "আপনার AI সঙ্গী। আপনার প্রতিদিনের যত্ন।",
        "name": "আপনার নাম",
        "phone": "মোবাইল নম্বর",
        "continue": "চালিয়ে যান",
        "verify": "যাচাই করে লগইন করুন",
        "otp_title": "আপনার মোবাইল নম্বর যাচাই করুন",
        "otp_prompt": "OTP লিখুন",
        "demo_otp": "ডেমো OTP: 123456",
        "invalid_name": "আপনার নাম লিখুন।",
        "invalid_phone": "সঠিক ১০ সংখ্যার নম্বর লিখুন।",
        "wrong_otp": "ভুল OTP। আবার চেষ্টা করুন।",
        "home": "হোম",
        "ai": "AI সঙ্গী",
        "quiz": "কুইজ",
        "reminders": "রিমাইন্ডার",
        "languages": "ভাষা",
        "profile": "প্রোফাইল",
        "logout": "লগ আউট",
        "hello": "নমস্কার",
        "what_do": "আজ আপনি কী করতে চান?",
        "open_ai": "AI সঙ্গী খুলুন",
        "start_quiz": "কুইজ শুরু করুন",
        "view_reminders": "রিমাইন্ডার দেখুন",
        "chat_title": "Careloop-এর সঙ্গে কথা বলুন",
        "choose_language": "আপনার ভাষা নির্বাচন করুন",
        "message": "Careloop-কে বার্তা পাঠান...",
        "thinking": "Careloop ভাবছে...",
        "clear_chat": "কথোপকথন মুছুন",
        "quiz_title": "আপনার জ্ঞান পরীক্ষা করুন!",
        "submit_quiz": "কুইজ জমা দিন",
        "your_score": "আপনার নম্বর",
        "excellent": "দারুণ! সম্পূর্ণ নম্বর!",
        "great": "খুব ভালো!",
        "improve": "ভালো চেষ্টা! শিখতে থাকুন!",
        "try_again": "আবার চেষ্টা করুন",
        "question": "প্রশ্ন",
        "correct": "সঠিক উত্তর",
        "all_questions": "সব প্রশ্নের উত্তর দিন।",
        "add_reminder": "রিমাইন্ডার যোগ করুন",
        "reminder": "রিমাইন্ডার",
        "reminder_date": "তারিখ",
        "reminder_time": "সময়",
        "save_reminder": "রিমাইন্ডার সংরক্ষণ করুন",
        "added": "রিমাইন্ডার যোগ করা হয়েছে!",
        "empty_reminder": "কোনো রিমাইন্ডার নেই।",
        "delete": "মুছুন",
        "reminder_list": "আপনার রিমাইন্ডার তালিকা",
        "language_title": "আপনার ভাষা নির্বাচন করুন",
        "save_language": "ভাষা সংরক্ষণ করুন",
        "language_saved": "ভাষা সংরক্ষিত হয়েছে!",
        "profile_title": "আমার প্রোফাইল",
        "account_details": "আপনার অ্যাকাউন্টের বিবরণ",
        "preferred": "পছন্দের ভাষা",
        "logged_in": "লগইন সফল হয়েছে!",
        "api_error": "AI উত্তর পাওয়া যায়নি। API বিলিং পরীক্ষা করুন।",
        "api_missing": "API কী সেট করা নেই।",
        "quiz_intro": "এই তিনটি প্রশ্নের উত্তর দিন।",
        "login_back": "ফিরে যান",
        "settings": "সেটিংস",
        "assistant_description": "আপনার AI সঙ্গীর সঙ্গে কথা বলুন।",
        "quiz_description": "একটি ছোট কুইজ খেলুন।",
        "reminder_description": "গুরুত্বপূর্ণ বিষয় মনে রাখুন।",
        "language_description": "আপনার পছন্দের ভাষা নির্বাচন করুন।",
        "no_chat": "Careloop-এর সঙ্গে কথা বলা শুরু করুন!",
        "question_1": "কোন গ্রহকে লাল গ্রহ বলা হয়?",
        "question_2": "অধিবর্ষে কত দিন থাকে?",
        "question_3": "বিশ্বের বৃহত্তম মহাসাগর কোনটি?",
        "option_earth": "পৃথিবী",
        "option_mars": "মঙ্গল",
        "option_jupiter": "বৃহস্পতি",
        "option_venus": "শুক্র",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "ভারত মহাসাগর",
        "option_atlantic": "আটলান্টিক মহাসাগর",
        "option_pacific": "প্রশান্ত মহাসাগর",
        "option_arctic": "আর্কটিক মহাসাগর",
        "quiz_results": "আপনার কুইজের ফলাফল",
        "saved": "সফলভাবে সংরক্ষিত!",
        "select_answer": "উত্তর নির্বাচন করুন",
        "quiz_zero": "শিখতে থাকুন! আবার চেষ্টা করুন।",
        "reminder_empty": "একটি রিমাইন্ডার লিখুন।",
        "logout_confirm": "আপনি লগ আউট করেছেন।"
    },

    "Marathi": {
        "welcome": "Careloop मध्ये आपले स्वागत आहे!",
        "tagline": "तुमचा AI साथीदार. तुमची दैनंदिन काळजी.",
        "name": "तुमचे नाव",
        "phone": "मोबाइल क्रमांक",
        "continue": "पुढे जा",
        "verify": "पडताळणी करून लॉगिन करा",
        "otp_title": "तुमचा मोबाइल क्रमांक पडताळा",
        "otp_prompt": "OTP टाका",
        "demo_otp": "डेमो OTP: 123456",
        "invalid_name": "कृपया तुमचे नाव टाका.",
        "invalid_phone": "योग्य 10 अंकी क्रमांक टाका.",
        "wrong_otp": "चुकीचा OTP. पुन्हा प्रयत्न करा.",
        "home": "मुख्यपृष्ठ",
        "ai": "AI साथीदार",
        "quiz": "प्रश्नमंजुषा",
        "reminders": "स्मरणपत्रे",
        "languages": "भाषा",
        "profile": "प्रोफाइल",
        "logout": "लॉग आउट",
        "hello": "नमस्कार",
        "what_do": "आज तुम्हाला काय करायचे आहे?",
        "open_ai": "AI साथीदार उघडा",
        "start_quiz": "प्रश्नमंजुषा सुरू करा",
        "view_reminders": "स्मरणपत्रे पहा",
        "chat_title": "Careloop सोबत बोला",
        "choose_language": "तुमची भाषा निवडा",
        "message": "Careloop ला संदेश पाठवा...",
        "thinking": "Careloop विचार करत आहे...",
        "clear_chat": "संभाषण पुसून टाका",
        "quiz_title": "तुमचे ज्ञान तपासा!",
        "submit_quiz": "प्रश्नमंजुषा सबमिट करा",
        "your_score": "तुमचे गुण",
        "excellent": "उत्कृष्ट! पूर्ण गुण!",
        "great": "छान काम!",
        "improve": "चांगला प्रयत्न! शिकत राहा!",
        "try_again": "पुन्हा प्रयत्न करा",
        "question": "प्रश्न",
        "correct": "योग्य उत्तर",
        "all_questions": "सर्व प्रश्नांची उत्तरे द्या.",
        "add_reminder": "स्मरणपत्र जोडा",
        "reminder": "स्मरणपत्र",
        "reminder_date": "तारीख",
        "reminder_time": "वेळ",
        "save_reminder": "स्मरणपत्र जतन करा",
        "added": "स्मरणपत्र जोडले!",
        "empty_reminder": "अद्याप स्मरणपत्रे नाहीत.",
        "delete": "हटवा",
        "reminder_list": "तुमची स्मरणपत्रे",
        "language_title": "तुमची भाषा निवडा",
        "save_language": "भाषा जतन करा",
        "language_saved": "भाषा जतन केली!",
        "profile_title": "माझे प्रोफाइल",
        "account_details": "तुमच्या खात्याचे तपशील",
        "preferred": "आवडती भाषा",
        "logged_in": "लॉगिन यशस्वी!",
        "api_error": "AI उत्तर मिळाले नाही. API बिलिंग तपासा.",
        "api_missing": "API की सेट केलेली नाही.",
        "quiz_intro": "या तीन प्रश्नांची उत्तरे द्या.",
        "login_back": "मागे",
        "settings": "सेटिंग्ज",
        "assistant_description": "तुमच्या AI साथीदाराशी बोला.",
        "quiz_description": "एक छोटी प्रश्नमंजुषा खेळा.",
        "reminder_description": "महत्त्वाच्या गोष्टी लक्षात ठेवा.",
        "language_description": "तुमची आवडती भाषा निवडा.",
        "no_chat": "Careloop सोबत संवाद सुरू करा!",
        "question_1": "लाल ग्रह म्हणून कोणत्या ग्रहाला ओळखले जाते?",
        "question_2": "लीप वर्षात किती दिवस असतात?",
        "question_3": "जगातील सर्वात मोठा महासागर कोणता?",
        "option_earth": "पृथ्वी",
        "option_mars": "मंगळ",
        "option_jupiter": "गुरू",
        "option_venus": "शुक्र",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "हिंदी महासागर",
        "option_atlantic": "अटलांटिक महासागर",
        "option_pacific": "प्रशांत महासागर",
        "option_arctic": "आर्क्टिक महासागर",
        "quiz_results": "तुमचा निकाल",
        "saved": "यशस्वीरित्या जतन केले!",
        "select_answer": "उत्तर निवडा",
        "quiz_zero": "शिकत राहा! पुन्हा प्रयत्न करा.",
        "reminder_empty": "कृपया स्मरणपत्र लिहा.",
        "logout_confirm": "तुम्ही लॉग आउट केले आहे."
    },

    "Gujarati": {
        "welcome": "Careloop માં આપનું સ્વાગત છે!",
        "tagline": "તમારો AI સાથી. તમારી દૈનિક સંભાળ.",
        "name": "તમારું નામ",
        "phone": "મોબાઇલ નંબર",
        "continue": "ચાલુ રાખો",
        "verify": "ચકાસો અને લોગિન કરો",
        "otp_title": "તમારો મોબાઇલ નંબર ચકાસો",
        "otp_prompt": "OTP દાખલ કરો",
        "demo_otp": "ડેમો OTP: 123456",
        "invalid_name": "કૃપા કરીને તમારું નામ દાખલ કરો.",
        "invalid_phone": "યોગ્ય 10 અંકનો નંબર દાખલ કરો.",
        "wrong_otp": "ખોટો OTP. ફરી પ્રયાસ કરો.",
        "home": "હોમ",
        "ai": "AI સાથી",
        "quiz": "ક્વિઝ",
        "reminders": "રિમાઇન્ડર",
        "languages": "ભાષાઓ",
        "profile": "પ્રોફાઇલ",
        "logout": "લોગ આઉટ",
        "hello": "નમસ્તે",
        "what_do": "આજે તમે શું કરવા માંગો છો?",
        "open_ai": "AI સાથી ખોલો",
        "start_quiz": "ક્વિઝ શરૂ કરો",
        "view_reminders": "રિમાઇન્ડર જુઓ",
        "chat_title": "Careloop સાથે વાત કરો",
        "choose_language": "તમારી ભાષા પસંદ કરો",
        "message": "Careloop ને સંદેશ મોકલો...",
        "thinking": "Careloop વિચારી રહ્યું છે...",
        "clear_chat": "વાતચીત સાફ કરો",
        "quiz_title": "તમારા જ્ઞાનની કસોટી કરો!",
        "submit_quiz": "ક્વિઝ સબમિટ કરો",
        "your_score": "તમારા ગુણ",
        "excellent": "શાનદાર! સંપૂર્ણ ગુણ!",
        "great": "ખૂબ સરસ!",
        "improve": "સારો પ્રયાસ! શીખતા રહો!",
        "try_again": "ફરી પ્રયાસ કરો",
        "question": "પ્રશ્ન",
        "correct": "સાચો જવાબ",
        "all_questions": "બધા પ્રશ્નોના જવાબ આપો.",
        "add_reminder": "રિમાઇન્ડર ઉમેરો",
        "reminder": "રિમાઇન્ડર",
        "reminder_date": "તારીખ",
        "reminder_time": "સમય",
        "save_reminder": "રિમાઇન્ડર સાચવો",
        "added": "રિમાઇન્ડર ઉમેરાયું!",
        "empty_reminder": "હજુ કોઈ રિમાઇન્ડર નથી.",
        "delete": "કાઢી નાખો",
        "reminder_list": "તમારા રિમાઇન્ડર",
        "language_title": "તમારી ભાષા પસંદ કરો",
        "save_language": "ભાષા સાચવો",
        "language_saved": "ભાષા સાચવાઈ!",
        "profile_title": "મારી પ્રોફાઇલ",
        "account_details": "તમારા ખાતાની વિગતો",
        "preferred": "પસંદગીની ભાષા",
        "logged_in": "લોગિન સફળ!",
        "api_error": "AI જવાબ મળી શક્યો નથી. API બિલિંગ તપાસો.",
        "api_missing": "API કી સેટ નથી.",
        "quiz_intro": "આ ત્રણ પ્રશ્નોના જવાબ આપો.",
        "login_back": "પાછા",
        "settings": "સેટિંગ્સ",
        "assistant_description": "તમારા AI સાથી સાથે વાત કરો.",
        "quiz_description": "એક નાની ક્વિઝ રમો.",
        "reminder_description": "મહત્વપૂર્ણ બાબતો યાદ રાખો.",
        "language_description": "તમારી પસંદગીની ભાષા પસંદ કરો.",
        "no_chat": "Careloop સાથે વાતચીત શરૂ કરો!",
        "question_1": "કયા ગ્રહને લાલ ગ્રહ કહેવામાં આવે છે?",
        "question_2": "લીપ વર્ષમાં કેટલા દિવસ હોય છે?",
        "question_3": "વિશ્વનો સૌથી મોટો મહાસાગર કયો છે?",
        "option_earth": "પૃથ્વી",
        "option_mars": "મંગળ",
        "option_jupiter": "ગુરુ",
        "option_venus": "શુક્ર",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "હિંદ મહાસાગર",
        "option_atlantic": "એટલાન્ટિક મહાસાગર",
        "option_pacific": "પ્રશાંત મહાસાગર",
        "option_arctic": "આર્કટિક મહાસાગર",
        "quiz_results": "તમારા ક્વિઝ પરિણામો",
        "saved": "સફળતાપૂર્વક સાચવાયું!",
        "select_answer": "જવાબ પસંદ કરો",
        "quiz_zero": "શીખતા રહો! ફરી પ્રયાસ કરો.",
        "reminder_empty": "કૃપા કરીને રિમાઇન્ડર લખો.",
        "logout_confirm": "તમે લોગ આઉટ થયા છો."
    },

    "Punjabi": {
        "welcome": "Careloop ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ!",
        "tagline": "ਤੁਹਾਡਾ AI ਸਾਥੀ। ਤੁਹਾਡੀ ਰੋਜ਼ਾਨਾ ਦੇਖਭਾਲ।",
        "name": "ਤੁਹਾਡਾ ਨਾਮ",
        "phone": "ਮੋਬਾਈਲ ਨੰਬਰ",
        "continue": "ਜਾਰੀ ਰੱਖੋ",
        "verify": "ਤਸਦੀਕ ਕਰੋ ਅਤੇ ਲੌਗਇਨ ਕਰੋ",
        "otp_title": "ਆਪਣਾ ਮੋਬਾਈਲ ਨੰਬਰ ਤਸਦੀਕ ਕਰੋ",
        "otp_prompt": "OTP ਦਰਜ ਕਰੋ",
        "demo_otp": "ਡੈਮੋ OTP: 123456",
        "invalid_name": "ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ ਨਾਮ ਦਰਜ ਕਰੋ।",
        "invalid_phone": "ਸਹੀ 10 ਅੰਕਾਂ ਦਾ ਨੰਬਰ ਦਰਜ ਕਰੋ।",
        "wrong_otp": "ਗਲਤ OTP। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        "home": "ਮੁੱਖ ਪੰਨਾ",
        "ai": "AI ਸਾਥੀ",
        "quiz": "ਕੁਇਜ਼",
        "reminders": "ਯਾਦ-ਦਿਹਾਨੀਆਂ",
        "languages": "ਭਾਸ਼ਾਵਾਂ",
        "profile": "ਪ੍ਰੋਫ਼ਾਈਲ",
        "logout": "ਲੌਗ ਆਉਟ",
        "hello": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
        "what_do": "ਅੱਜ ਤੁਸੀਂ ਕੀ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "open_ai": "AI ਸਾਥੀ ਖੋਲ੍ਹੋ",
        "start_quiz": "ਕੁਇਜ਼ ਸ਼ੁਰੂ ਕਰੋ",
        "view_reminders": "ਯਾਦ-ਦਿਹਾਨੀਆਂ ਵੇਖੋ",
        "chat_title": "Careloop ਨਾਲ ਗੱਲ ਕਰੋ",
        "choose_language": "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ",
        "message": "Careloop ਨੂੰ ਸੁਨੇਹਾ ਭੇਜੋ...",
        "thinking": "Careloop ਸੋਚ ਰਿਹਾ ਹੈ...",
        "clear_chat": "ਗੱਲਬਾਤ ਸਾਫ਼ ਕਰੋ",
        "quiz_title": "ਆਪਣੇ ਗਿਆਨ ਦੀ ਜਾਂਚ ਕਰੋ!",
        "submit_quiz": "ਕੁਇਜ਼ ਜਮ੍ਹਾਂ ਕਰੋ",
        "your_score": "ਤੁਹਾਡੇ ਅੰਕ",
        "excellent": "ਸ਼ਾਨਦਾਰ! ਪੂਰੇ ਅੰਕ!",
        "great": "ਬਹੁਤ ਵਧੀਆ!",
        "improve": "ਚੰਗੀ ਕੋਸ਼ਿਸ਼! ਸਿੱਖਦੇ ਰਹੋ!",
        "try_again": "ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
        "question": "ਸਵਾਲ",
        "correct": "ਸਹੀ ਜਵਾਬ",
        "all_questions": "ਸਾਰੇ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿਓ।",
        "add_reminder": "ਯਾਦ-ਦਿਹਾਨੀ ਸ਼ਾਮਲ ਕਰੋ",
        "reminder": "ਯਾਦ-ਦਿਹਾਨੀ",
        "reminder_date": "ਤਾਰੀਖ",
        "reminder_time": "ਸਮਾਂ",
        "save_reminder": "ਯਾਦ-ਦਿਹਾਨੀ ਸੁਰੱਖਿਅਤ ਕਰੋ",
        "added": "ਯਾਦ-ਦਿਹਾਨੀ ਸ਼ਾਮਲ ਕੀਤੀ ਗਈ!",
        "empty_reminder": "ਕੋਈ ਯਾਦ-ਦਿਹਾਨੀ ਨਹੀਂ ਹੈ।",
        "delete": "ਮਿਟਾਓ",
        "reminder_list": "ਤੁਹਾਡੀਆਂ ਯਾਦ-ਦਿਹਾਨੀਆਂ",
        "language_title": "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ",
        "save_language": "ਭਾਸ਼ਾ ਸੁਰੱਖਿਅਤ ਕਰੋ",
        "language_saved": "ਭਾਸ਼ਾ ਸੁਰੱਖਿਅਤ ਕੀਤੀ ਗਈ!",
        "profile_title": "ਮੇਰੀ ਪ੍ਰੋਫ਼ਾਈਲ",
        "account_details": "ਤੁਹਾਡੇ ਖਾਤੇ ਦੇ ਵੇਰਵੇ",
        "preferred": "ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ",
        "logged_in": "ਲੌਗਇਨ ਸਫਲ!",
        "api_error": "AI ਜਵਾਬ ਨਹੀਂ ਮਿਲਿਆ। API ਬਿਲਿੰਗ ਜਾਂਚੋ।",
        "api_missing": "API ਕੁੰਜੀ ਸੈੱਟ ਨਹੀਂ ਹੈ।",
        "quiz_intro": "ਇਨ੍ਹਾਂ ਤਿੰਨ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿਓ।",
        "login_back": "ਵਾਪਸ",
        "settings": "ਸੈਟਿੰਗਾਂ",
        "assistant_description": "ਆਪਣੇ AI ਸਾਥੀ ਨਾਲ ਗੱਲ ਕਰੋ।",
        "quiz_description": "ਇੱਕ ਛੋਟਾ ਕੁਇਜ਼ ਖੇਡੋ।",
        "reminder_description": "ਮਹੱਤਵਪੂਰਨ ਗੱਲਾਂ ਯਾਦ ਰੱਖੋ।",
        "language_description": "ਆਪਣੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਚੁਣੋ।",
        "no_chat": "Careloop ਨਾਲ ਗੱਲਬਾਤ ਸ਼ੁਰੂ ਕਰੋ!",
        "question_1": "ਕਿਹੜੇ ਗ੍ਰਹਿ ਨੂੰ ਲਾਲ ਗ੍ਰਹਿ ਕਿਹਾ ਜਾਂਦਾ ਹੈ?",
        "question_2": "ਲੀਪ ਸਾਲ ਵਿੱਚ ਕਿੰਨੇ ਦਿਨ ਹੁੰਦੇ ਹਨ?",
        "question_3": "ਦੁਨੀਆ ਦਾ ਸਭ ਤੋਂ ਵੱਡਾ ਸਮੁੰਦਰ ਕਿਹੜਾ ਹੈ?",
        "option_earth": "ਧਰਤੀ",
        "option_mars": "ਮੰਗਲ",
        "option_jupiter": "ਬ੍ਰਹਿਸਪਤੀ",
        "option_venus": "ਸ਼ੁੱਕਰ",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "ਹਿੰਦ ਮਹਾਂਸਾਗਰ",
        "option_atlantic": "ਅਟਲਾਂਟਿਕ ਮਹਾਂਸਾਗਰ",
        "option_pacific": "ਪ੍ਰਸ਼ਾਂਤ ਮਹਾਂਸਾਗਰ",
        "option_arctic": "ਆਰਕਟਿਕ ਮਹਾਂਸਾਗਰ",
        "quiz_results": "ਤੁਹਾਡੇ ਕੁਇਜ਼ ਦੇ ਨਤੀਜੇ",
        "saved": "ਸਫਲਤਾਪੂਰਵਕ ਸੁਰੱਖਿਅਤ ਕੀਤਾ!",
        "select_answer": "ਜਵਾਬ ਚੁਣੋ",
        "quiz_zero": "ਸਿੱਖਦੇ ਰਹੋ! ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        "reminder_empty": "ਕਿਰਪਾ ਕਰਕੇ ਯਾਦ-ਦਿਹਾਨੀ ਲਿਖੋ।",
        "logout_confirm": "ਤੁਸੀਂ ਲੌਗ ਆਉਟ ਕਰ ਦਿੱਤਾ ਹੈ।"
    },

    "Arabic": {
        "welcome": "مرحباً بك في Careloop!",
        "tagline": "رفيقك الذكي. رعايتك اليومية.",
        "name": "اسمك",
        "phone": "رقم الهاتف",
        "continue": "متابعة",
        "verify": "تحقق وتسجيل الدخول",
        "otp_title": "تحقق من رقم هاتفك",
        "otp_prompt": "أدخل رمز OTP",
        "demo_otp": "رمز تجريبي: 123456",
        "invalid_name": "يرجى إدخال اسمك.",
        "invalid_phone": "أدخل رقم هاتف صحيحاً من 10 أرقام.",
        "wrong_otp": "رمز غير صحيح. حاول مرة أخرى.",
        "home": "الرئيسية",
        "ai": "المرافق الذكي",
        "quiz": "الاختبارات",
        "reminders": "التذكيرات",
        "languages": "اللغات",
        "profile": "الملف الشخصي",
        "logout": "تسجيل الخروج",
        "hello": "مرحباً",
        "what_do": "ماذا تريد أن تفعل اليوم؟",
        "open_ai": "افتح المرافق الذكي",
        "start_quiz": "ابدأ الاختبار",
        "view_reminders": "عرض التذكيرات",
        "chat_title": "تحدث مع Careloop",
        "choose_language": "اختر لغتك",
        "message": "أرسل رسالة إلى Careloop...",
        "thinking": "Careloop يفكر...",
        "clear_chat": "مسح المحادثة",
        "quiz_title": "اختبر معلوماتك!",
        "submit_quiz": "إرسال الاختبار",
        "your_score": "درجتك",
        "excellent": "ممتاز! نتيجة كاملة!",
        "great": "عمل رائع!",
        "improve": "محاولة جيدة! استمر في التعلم!",
        "try_again": "حاول مرة أخرى",
        "question": "السؤال",
        "correct": "الإجابة الصحيحة",
        "all_questions": "يرجى الإجابة عن جميع الأسئلة.",
        "add_reminder": "إضافة تذكير",
        "reminder": "تذكير",
        "reminder_date": "التاريخ",
        "reminder_time": "الوقت",
        "save_reminder": "حفظ التذكير",
        "added": "تمت إضافة التذكير!",
        "empty_reminder": "لا توجد تذكيرات.",
        "delete": "حذف",
        "reminder_list": "قائمة التذكيرات",
        "language_title": "اختر لغتك",
        "save_language": "حفظ اللغة",
        "language_saved": "تم حفظ اللغة!",
        "profile_title": "ملفي الشخصي",
        "account_details": "تفاصيل حسابك",
        "preferred": "اللغة المفضلة",
        "logged_in": "تم تسجيل الدخول بنجاح!",
        "api_error": "تعذر الحصول على رد الذكاء الاصطناعي. تحقق من الفوترة.",
        "api_missing": "مفتاح API غير مُعد.",
        "quiz_intro": "أجب عن هذه الأسئلة الثلاثة.",
        "login_back": "رجوع",
        "settings": "الإعدادات",
        "assistant_description": "تحدث مع رفيقك الذكي.",
        "quiz_description": "اختبر نفسك باختبار قصير.",
        "reminder_description": "تذكر الأشياء المهمة.",
        "language_description": "اختر لغتك المفضلة.",
        "no_chat": "ابدأ محادثة مع Careloop!",
        "question_1": "أي كوكب يُعرف بالكوكب الأحمر؟",
        "question_2": "كم يوماً في السنة الكبيسة؟",
        "question_3": "ما أكبر محيط في العالم؟",
        "option_earth": "الأرض",
        "option_mars": "المريخ",
        "option_jupiter": "المشتري",
        "option_venus": "الزهرة",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "المحيط الهندي",
        "option_atlantic": "المحيط الأطلسي",
        "option_pacific": "المحيط الهادئ",
        "option_arctic": "المحيط المتجمد الشمالي",
        "quiz_results": "نتائج الاختبار",
        "saved": "تم الحفظ بنجاح!",
        "select_answer": "اختر إجابتك",
        "quiz_zero": "واصل التعلم! حاول مرة أخرى.",
        "reminder_empty": "يرجى إدخال تذكير.",
        "logout_confirm": "تم تسجيل خروجك."
    },

    "French": {
        "welcome": "Bienvenue sur Careloop !",
        "tagline": "Votre compagnon IA. Votre bien-être quotidien.",
        "name": "Votre nom",
        "phone": "Numéro de téléphone",
        "continue": "Continuer",
        "verify": "Vérifier et se connecter",
        "otp_title": "Vérifiez votre numéro de téléphone",
        "otp_prompt": "Saisissez le code OTP",
        "demo_otp": "OTP de démonstration : 123456",
        "invalid_name": "Veuillez saisir votre nom.",
        "invalid_phone": "Saisissez un numéro valide à 10 chiffres.",
        "wrong_otp": "OTP incorrect. Réessayez.",
        "home": "Accueil",
        "ai": "Compagnon IA",
        "quiz": "Quiz",
        "reminders": "Rappels",
        "languages": "Langues",
        "profile": "Profil",
        "logout": "Déconnexion",
        "hello": "Bonjour",
        "what_do": "Que souhaitez-vous faire aujourd'hui ?",
        "open_ai": "Ouvrir le compagnon IA",
        "start_quiz": "Commencer un quiz",
        "view_reminders": "Voir les rappels",
        "chat_title": "Parlez avec Careloop",
        "choose_language": "Choisissez votre langue",
        "message": "Envoyer un message à Careloop...",
        "thinking": "Careloop réfléchit...",
        "clear_chat": "Effacer la conversation",
        "quiz_title": "Testez vos connaissances !",
        "submit_quiz": "Envoyer le quiz",
        "your_score": "Votre score",
        "excellent": "Excellent ! Score parfait !",
        "great": "Très bon travail !",
        "improve": "Bel effort ! Continuez à apprendre !",
        "try_again": "Réessayer",
        "question": "Question",
        "correct": "Bonne réponse",
        "all_questions": "Veuillez répondre à toutes les questions.",
        "add_reminder": "Ajouter un rappel",
        "reminder": "Rappel",
        "reminder_date": "Date",
        "reminder_time": "Heure",
        "save_reminder": "Enregistrer le rappel",
        "added": "Rappel ajouté !",
        "empty_reminder": "Aucun rappel pour le moment.",
        "delete": "Supprimer",
        "reminder_list": "Vos rappels",
        "language_title": "Choisissez votre langue",
        "save_language": "Enregistrer la langue",
        "language_saved": "Langue enregistrée !",
        "profile_title": "Mon profil",
        "account_details": "Détails de votre compte",
        "preferred": "Langue préférée",
        "logged_in": "Connexion réussie !",
        "api_error": "Impossible d'obtenir une réponse IA. Vérifiez la facturation.",
        "api_missing": "Clé API non configurée.",
        "quiz_intro": "Répondez à ces trois questions.",
        "login_back": "Retour",
        "settings": "Paramètres",
        "assistant_description": "Parlez avec votre compagnon IA.",
        "quiz_description": "Testez-vous avec un petit quiz.",
        "reminder_description": "Gardez en mémoire les choses importantes.",
        "language_description": "Choisissez votre langue préférée.",
        "no_chat": "Commencez une conversation avec Careloop !",
        "question_1": "Quelle planète est appelée la planète rouge ?",
        "question_2": "Combien de jours compte une année bissextile ?",
        "question_3": "Quel est le plus grand océan du monde ?",
        "option_earth": "Terre",
        "option_mars": "Mars",
        "option_jupiter": "Jupiter",
        "option_venus": "Vénus",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "Océan Indien",
        "option_atlantic": "Océan Atlantique",
        "option_pacific": "Océan Pacifique",
        "option_arctic": "Océan Arctique",
        "quiz_results": "Résultats du quiz",
        "saved": "Enregistré avec succès !",
        "select_answer": "Choisissez votre réponse",
        "quiz_zero": "Continuez à apprendre ! Réessayez.",
        "reminder_empty": "Veuillez saisir un rappel.",
        "logout_confirm": "Vous êtes déconnecté."
    },

    "Spanish": {
        "welcome": "¡Bienvenido a Careloop!",
        "tagline": "Tu compañero de IA. Tu cuidado diario.",
        "name": "Tu nombre",
        "phone": "Número de móvil",
        "continue": "Continuar",
        "verify": "Verificar e iniciar sesión",
        "otp_title": "Verifica tu número de móvil",
        "otp_prompt": "Introduce el OTP",
        "demo_otp": "OTP de demostración: 123456",
        "invalid_name": "Por favor, introduce tu nombre.",
        "invalid_phone": "Introduce un número válido de 10 dígitos.",
        "wrong_otp": "OTP incorrecto. Inténtalo de nuevo.",
        "home": "Inicio",
        "ai": "Compañero IA",
        "quiz": "Cuestionarios",
        "reminders": "Recordatorios",
        "languages": "Idiomas",
        "profile": "Perfil",
        "logout": "Cerrar sesión",
        "hello": "Hola",
        "what_do": "¿Qué te gustaría hacer hoy?",
        "open_ai": "Abrir compañero IA",
        "start_quiz": "Comenzar cuestionario",
        "view_reminders": "Ver recordatorios",
        "chat_title": "Habla con Careloop",
        "choose_language": "Elige tu idioma",
        "message": "Enviar mensaje a Careloop...",
        "thinking": "Careloop está pensando...",
        "clear_chat": "Borrar conversación",
        "quiz_title": "¡Pon a prueba tus conocimientos!",
        "submit_quiz": "Enviar cuestionario",
        "your_score": "Tu puntuación",
        "excellent": "¡Excelente! ¡Puntuación perfecta!",
        "great": "¡Muy buen trabajo!",
        "improve": "¡Buen intento! ¡Sigue aprendiendo!",
        "try_again": "Intentar de nuevo",
        "question": "Pregunta",
        "correct": "Respuesta correcta",
        "all_questions": "Responde todas las preguntas.",
        "add_reminder": "Añadir recordatorio",
        "reminder": "Recordatorio",
        "reminder_date": "Fecha",
        "reminder_time": "Hora",
        "save_reminder": "Guardar recordatorio",
        "added": "¡Recordatorio añadido!",
        "empty_reminder": "Todavía no tienes recordatorios.",
        "delete": "Eliminar",
        "reminder_list": "Tus recordatorios",
        "language_title": "Elige tu idioma",
        "save_language": "Guardar idioma",
        "language_saved": "¡Idioma guardado!",
        "profile_title": "Mi perfil",
        "account_details": "Detalles de tu cuenta",
        "preferred": "Idioma preferido",
        "logged_in": "¡Inicio de sesión correcto!",
        "api_error": "No se pudo obtener una respuesta de IA. Revisa la facturación.",
        "api_missing": "La clave API no está configurada.",
        "quiz_intro": "Responde estas tres preguntas.",
        "login_back": "Volver",
        "settings": "Configuración",
        "assistant_description": "Habla con tu compañero de IA.",
        "quiz_description": "Participa en un pequeño cuestionario.",
        "reminder_description": "Recuerda las cosas importantes.",
        "language_description": "Elige tu idioma preferido.",
        "no_chat": "¡Comienza una conversación con Careloop!",
        "question_1": "¿Qué planeta se conoce como el planeta rojo?",
        "question_2": "¿Cuántos días tiene un año bisiesto?",
        "question_3": "¿Cuál es el océano más grande del mundo?",
        "option_earth": "Tierra",
        "option_mars": "Marte",
        "option_jupiter": "Júpiter",
        "option_venus": "Venus",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "Océano Índico",
        "option_atlantic": "Océano Atlántico",
        "option_pacific": "Océano Pacífico",
        "option_arctic": "Océano Ártico",
        "quiz_results": "Resultados del cuestionario",
        "saved": "¡Guardado correctamente!",
        "select_answer": "Elige tu respuesta",
        "quiz_zero": "¡Sigue aprendiendo! Inténtalo de nuevo.",
        "reminder_empty": "Introduce un recordatorio.",
        "logout_confirm": "Has cerrado sesión."
    },

    "German": {
        "welcome": "Willkommen bei Careloop!",
        "tagline": "Dein KI-Begleiter. Deine tägliche Unterstützung.",
        "name": "Dein Name",
        "phone": "Mobilnummer",
        "continue": "Weiter",
        "verify": "Bestätigen und anmelden",
        "otp_title": "Bestätige deine Mobilnummer",
        "otp_prompt": "OTP eingeben",
        "demo_otp": "Demo-OTP: 123456",
        "invalid_name": "Bitte gib deinen Namen ein.",
        "invalid_phone": "Gib eine gültige 10-stellige Nummer ein.",
        "wrong_otp": "Falsches OTP. Versuche es erneut.",
        "home": "Startseite",
        "ai": "KI-Begleiter",
        "quiz": "Quiz",
        "reminders": "Erinnerungen",
        "languages": "Sprachen",
        "profile": "Profil",
        "logout": "Abmelden",
        "hello": "Hallo",
        "what_do": "Was möchtest du heute machen?",
        "open_ai": "KI-Begleiter öffnen",
        "start_quiz": "Quiz starten",
        "view_reminders": "Erinnerungen anzeigen",
        "chat_title": "Sprich mit Careloop",
        "choose_language": "Wähle deine Sprache",
        "message": "Nachricht an Careloop...",
        "thinking": "Careloop denkt nach...",
        "clear_chat": "Gespräch löschen",
        "quiz_title": "Teste dein Wissen!",
        "submit_quiz": "Quiz absenden",
        "your_score": "Deine Punktzahl",
        "excellent": "Ausgezeichnet! Volle Punktzahl!",
        "great": "Sehr gut gemacht!",
        "improve": "Guter Versuch! Lerne weiter!",
        "try_again": "Erneut versuchen",
        "question": "Frage",
        "correct": "Richtige Antwort",
        "all_questions": "Bitte beantworte alle Fragen.",
        "add_reminder": "Erinnerung hinzufügen",
        "reminder": "Erinnerung",
        "reminder_date": "Datum",
        "reminder_time": "Uhrzeit",
        "save_reminder": "Erinnerung speichern",
        "added": "Erinnerung hinzugefügt!",
        "empty_reminder": "Du hast noch keine Erinnerungen.",
        "delete": "Löschen",
        "reminder_list": "Deine Erinnerungen",
        "language_title": "Wähle deine Sprache",
        "save_language": "Sprache speichern",
        "language_saved": "Sprache gespeichert!",
        "profile_title": "Mein Profil",
        "account_details": "Deine Kontodaten",
        "preferred": "Bevorzugte Sprache",
        "logged_in": "Anmeldung erfolgreich!",
        "api_error": "Keine KI-Antwort erhalten. Bitte Abrechnung prüfen.",
        "api_missing": "API-Schlüssel ist nicht eingerichtet.",
        "quiz_intro": "Beantworte diese drei Fragen.",
        "login_back": "Zurück",
        "settings": "Einstellungen",
        "assistant_description": "Sprich mit deinem KI-Begleiter.",
        "quiz_description": "Mach ein kurzes Quiz.",
        "reminder_description": "Behalte wichtige Dinge im Blick.",
        "language_description": "Wähle deine bevorzugte Sprache.",
        "no_chat": "Beginne ein Gespräch mit Careloop!",
        "question_1": "Welcher Planet wird der rote Planet genannt?",
        "question_2": "Wie viele Tage hat ein Schaltjahr?",
        "question_3": "Welcher ist der größte Ozean der Welt?",
        "option_earth": "Erde",
        "option_mars": "Mars",
        "option_jupiter": "Jupiter",
        "option_venus": "Venus",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "Indischer Ozean",
        "option_atlantic": "Atlantischer Ozean",
        "option_pacific": "Pazifischer Ozean",
        "option_arctic": "Arktischer Ozean",
        "quiz_results": "Deine Quiz-Ergebnisse",
        "saved": "Erfolgreich gespeichert!",
        "select_answer": "Wähle deine Antwort",
        "quiz_zero": "Lerne weiter! Versuche es erneut.",
        "reminder_empty": "Bitte gib eine Erinnerung ein.",
        "logout_confirm": "Du wurdest abgemeldet."
    },

    "Japanese": {
        "welcome": "Careloopへようこそ！",
        "tagline": "あなたのAIパートナー。毎日のケア。",
        "name": "お名前",
        "phone": "携帯電話番号",
        "continue": "続ける",
        "verify": "確認してログイン",
        "otp_title": "電話番号を確認してください",
        "otp_prompt": "OTPを入力",
        "demo_otp": "デモOTP: 123456",
        "invalid_name": "名前を入力してください。",
        "invalid_phone": "正しい10桁の番号を入力してください。",
        "wrong_otp": "OTPが正しくありません。もう一度お試しください。",
        "home": "ホーム",
        "ai": "AIパートナー",
        "quiz": "クイズ",
        "reminders": "リマインダー",
        "languages": "言語",
        "profile": "プロフィール",
        "logout": "ログアウト",
        "hello": "こんにちは",
        "what_do": "今日は何をしたいですか？",
        "open_ai": "AIパートナーを開く",
        "start_quiz": "クイズを開始",
        "view_reminders": "リマインダーを見る",
        "chat_title": "Careloopと話す",
        "choose_language": "言語を選択",
        "message": "Careloopにメッセージ...",
        "thinking": "Careloopが考えています...",
        "clear_chat": "会話を消去",
        "quiz_title": "知識をテストしましょう！",
        "submit_quiz": "クイズを送信",
        "your_score": "あなたの得点",
        "excellent": "素晴らしい！満点です！",
        "great": "よくできました！",
        "improve": "いい挑戦です！学び続けましょう！",
        "try_again": "もう一度試す",
        "question": "質問",
        "correct": "正解",
        "all_questions": "すべての質問に答えてください。",
        "add_reminder": "リマインダーを追加",
        "reminder": "リマインダー",
        "reminder_date": "日付",
        "reminder_time": "時間",
        "save_reminder": "保存",
        "added": "リマインダーを追加しました！",
        "empty_reminder": "リマインダーはありません。",
        "delete": "削除",
        "reminder_list": "リマインダー一覧",
        "language_title": "言語を選択",
        "save_language": "言語を保存",
        "language_saved": "言語を保存しました！",
        "profile_title": "プロフィール",
        "account_details": "アカウント情報",
        "preferred": "優先言語",
        "logged_in": "ログイン成功！",
        "api_error": "AIの回答を取得できません。API請求を確認してください。",
        "api_missing": "APIキーが設定されていません。",
        "quiz_intro": "この3つの質問に答えてください。",
        "login_back": "戻る",
        "settings": "設定",
        "assistant_description": "AIパートナーと話しましょう。",
        "quiz_description": "簡単なクイズに挑戦しましょう。",
        "reminder_description": "大切なことを忘れないようにしましょう。",
        "language_description": "お好みの言語を選んでください。",
        "no_chat": "Careloopとの会話を始めましょう！",
        "question_1": "赤い惑星と呼ばれる惑星はどれですか？",
        "question_2": "うるう年は何日ありますか？",
        "question_3": "世界最大の海洋はどれですか？",
        "option_earth": "地球",
        "option_mars": "火星",
        "option_jupiter": "木星",
        "option_venus": "金星",
        "option_365": "365",
        "option_366": "366",
        "option_364": "364",
        "option_360": "360",
        "option_indian": "インド洋",
        "option_atlantic": "大西洋",
        "option_pacific": "太平洋",
        "option_arctic": "北極海",
        "quiz_results": "クイズの結果",
        "saved": "正常に保存しました！",
        "select_answer": "答えを選択",
        "quiz_zero": "学び続けましょう！もう一度挑戦してください。",
        "reminder_empty": "リマインダーを入力してください。",
        "logout_confirm": "ログアウトしました。"
    }
}

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "logged_in": False,
    "otp_sent": False,
    "user_name": "",
    "phone": "",
    "page": "home",
    "language": "English",
    "messages": [],
    "reminders": [],
    "quiz_score": None,
    "quiz_answers": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# TRANSLATION HELPER
# =========================================================

def tr(key):
    language = st.session_state.language
    return TRANSLATIONS[language].get(
        key,
        TRANSLATIONS["English"].get(key, key)
    )

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #edf5ff, #f8f3ff);
}
.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
}
.careloop-title {
    text-align: center;
    color: #3157a4;
    font-size: 42px;
    font-weight: 800;
}
.careloop-subtitle {
    text-align: center;
    color: #68758e;
    margin-bottom: 30px;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="careloop-title">💙 Careloop</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="careloop-subtitle">{tr("tagline")}</div>',
    unsafe_allow_html=True
)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    # Language selector available before login
    st.selectbox(
        tr("choose_language"),
        list(TRANSLATIONS.keys()),
        key="language"
    )

    if not st.session_state.otp_sent:

        st.title(tr("welcome"))

        with st.form("login_form"):

            name = st.text_input(tr("name"))
            phone = st.text_input(
                tr("phone"),
                max_chars=10
            )

            submitted = st.form_submit_button(
                tr("continue"),
                use_container_width=True
            )

        if submitted:
            if not name.strip():
                st.error(tr("invalid_name"))
            elif not phone.isdigit() or len(phone) != 10:
                st.error(tr("invalid_phone"))
            else:
                st.session_state.user_name = name.strip()
                st.session_state.phone = phone
                st.session_state.otp_sent = True
                st.rerun()

    else:

        st.title(tr("otp_title"))
        st.write(tr("demo_otp"))

        with st.form("otp_form"):

            otp = st.text_input(
                tr("otp_prompt"),
                type="password",
                max_chars=6
            )

            verified = st.form_submit_button(
                tr("verify"),
                use_container_width=True
            )

        if verified:
            if otp == "123456":
                st.session_state.logged_in = True
                st.session_state.otp_sent = False
                st.session_state.page = "home"
                st.success(tr("logged_in"))
                st.rerun()
            else:
                st.error(tr("wrong_otp"))

        if st.button(tr("login_back")):
            st.session_state.otp_sent = False
            st.rerun()

    st.stop()

# =========================================================
# NAVIGATION
# =========================================================

pages = {
    "home": "home",
    "ai": "ai",
    "quiz": "quiz",
    "reminders": "reminders",
    "languages": "languages",
    "profile": "profile"
}

with st.sidebar:

    st.title("💙 Careloop")
    st.write(f"{tr('hello')}, {st.session_state.user_name}!")

    st.selectbox(
        tr("choose_language"),
        list(TRANSLATIONS.keys()),
        key="language"
    )

    st.divider()

    page_keys = list(pages.keys())
    page_labels = [tr(key) for key in page_keys]

    current_index = page_keys.index(
        st.session_state.page
    )

    selected_label = st.radio(
        tr("settings"),
        page_labels,
        index=current_index
    )

    st.session_state.page = page_keys[
        page_labels.index(selected_label)
    ]

    st.divider()

    if st.button(tr("logout"), use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.otp_sent = False
        st.session_state.messages = []
        st.session_state.page = "home"

        st.rerun()

# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.title(f"{tr('hello')}, {st.session_state.user_name} 👋")

    st.subheader(tr("welcome"))
    st.write(tr("what_do"))

    st.divider()

    st.markdown(f"### 🤖 {tr('ai')}")
    st.write(tr("assistant_description"))

    if st.button(tr("open_ai"), use_container_width=True):
        st.session_state.page = "ai"
        st.rerun()

    st.divider()

    st.markdown(f"### 🧠 {tr('quiz')}")
    st.write(tr("quiz_description"))

    if st.button(tr("start_quiz"), use_container_width=True):
        st.session_state.page = "quiz"
        st.rerun()

    st.divider()

    st.markdown(f"### ⏰ {tr('reminders')}")
    st.write(tr("reminder_description"))

    if st.button(tr("view_reminders"), use_container_width=True):
        st.session_state.page = "reminders"
        st.rerun()

# =========================================================
# AI COMPANION
# =========================================================

elif st.session_state.page == "ai":

    st.title(f"🤖 {tr('chat_title')}")

    st.caption(
        f"{tr('preferred')}: {st.session_state.language}"
    )

    if st.button(tr("clear_chat")):
        st.session_state.messages = []
        st.rerun()

    if not st.session_state.messages:
        st.info(tr("no_chat"))

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(tr("message"))

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            api_key = st.secrets.get("OPENAI_API_KEY", "")

            if not api_key:
                st.error(tr("api_missing"))
                st.stop()

            client = OpenAI(api_key=api_key)

            instructions = f"""
You are Careloop, a friendly and intelligent AI companion.

The selected language is {st.session_state.language}.

Always respond in {st.session_state.language}.
Understand messages written in other languages.
Do not change the response language unless the user changes
the language selection.
Maintain conversation context.
Be helpful, honest and conversational.
Do not pretend to be a doctor.
"""

            with st.chat_message("assistant"):

                with st.spinner(tr("thinking")):

                    response = client.responses.create(
                        model=MODEL,
                        instructions=instructions,
                        input=st.session_state.messages
                    )

                    answer = response.output_text

                    if not answer:
                        answer = "Please try again."

                    st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:
            st.error(tr("api_error"))
            st.caption(str(error))

# =========================================================
# QUIZZES
# =========================================================

elif st.session_state.page == "quiz":

    st.title(f"🧠 {tr('quiz_title')}")
    st.write(tr("quiz_intro"))

    quiz_data = [
        {
            "question": "question_1",
            "options": [
                "option_earth",
                "option_mars",
                "option_jupiter",
                "option_venus"
            ],
            "answer": "option_mars"
        },
        {
            "question": "question_2",
            "options": [
                "option_365",
                "option_366",
                "option_364",
                "option_360"
            ],
            "answer": "option_366"
        },
        {
            "question": "question_3",
            "options": [
                "option_indian",
                "option_atlantic",
                "option_pacific",
                "option_arctic"
            ],
            "answer": "option_pacific"
        }
    ]

    with st.form("quiz_form"):

        answers = []

        for index, question in enumerate(quiz_data):

            st.markdown(
                f"### {tr('question')} {index + 1}"
            )

            st.write(tr(question["question"]))

            option_keys = question["options"]

            selected = st.radio(
                tr("select_answer"),
                option_keys,
                format_func=tr,
                index=None,
                key=f"quiz_question_{index}"
            )

            answers.append(selected)

            st.divider()

        submitted = st.form_submit_button(
            tr("submit_quiz"),
            use_container_width=True
        )

    if submitted:

        if any(answer is None for answer in answers):
            st.warning(tr("all_questions"))

        else:

            score = sum(
                answers[index] == question["answer"]
                for index, question in enumerate(quiz_data)
            )

            st.session_state.quiz_score = score
            st.session_state.quiz_answers = answers

    if st.session_state.quiz_score is not None:

        score = st.session_state.quiz_score

        st.divider()
        st.subheader(tr("quiz_results"))

        st.metric(
            tr("your_score"),
            f"{score} / 3"
        )

        if score == 3:
            st.success(tr("excellent"))
        elif score == 2:
            st.success(tr("great"))
        elif score == 1:
            st.info(tr("improve"))
        else:
            st.info(tr("quiz_zero"))

        for index, question in enumerate(quiz_data):

            st.write(
                f"**{tr('question')} {index + 1}: "
                f"{tr(question['question'])}**"
            )

            st.write(
                f"{tr('correct')}: {tr(question['answer'])}"
            )

        if st.button(tr("try_again")):
            st.session_state.quiz_score = None
            st.session_state.quiz_answers = {}
            st.rerun()

# =========================================================
# REMINDERS
# =========================================================

elif st.session_state.page == "reminders":

    st.title(f"⏰ {tr('reminders')}")

    with st.form("reminder_form"):

        reminder_text = st.text_input(tr("reminder"))

        reminder_date = st.date_input(
            tr("reminder_date"),
            value=date.today()
        )

        reminder_time = st.time_input(
            tr("reminder_time"),
            value=time(9, 0)
        )

        submitted = st.form_submit_button(
            tr("save_reminder"),
            use_container_width=True
        )

    if submitted:

        if reminder_text.strip():

            st.session_state.reminders.append({
                "text": reminder_text.strip(),
                "date": reminder_date,
                "time": reminder_time
            })

            st.success(tr("added"))
            st.rerun()

        else:
            st.warning(tr("reminder_empty"))

    st.divider()
    st.subheader(tr("reminder_list"))

    if not st.session_state.reminders:

        st.info(tr("empty_reminder"))

    else:

        for index, reminder in enumerate(
            st.session_state.reminders
        ):

            st.write(f"**{reminder['text']}**")

            st.caption(
                f"{reminder['date']} • {reminder['time']}"
            )

            if st.button(
                tr("delete"),
                key=f"delete_reminder_{index}"
            ):

                st.session_state.reminders.pop(index)
                st.rerun()

            st.divider()

# =========================================================
# LANGUAGE PAGE
# =========================================================

elif st.session_state.page == "languages":

    st.title(f"🌍 {tr('language_title')}")

    st.write(tr("language_description"))

    selected = st.selectbox(
        tr("choose_language"),
        list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(
            st.session_state.language
        ),
        key="language_page_selector"
    )

    if st.button(tr("save_language"), use_container_width=True):

        st.session_state.language = selected
        st.success(
            TRANSLATIONS[selected]["language_saved"]
        )
        st.rerun()

# =========================================================
# PROFILE PAGE
# =========================================================

elif st.session_state.page == "profile":

    st.title(f"👤 {tr('profile_title')}")

    st.write(tr("account_details"))

    st.text_input(
        tr("name"),
        value=st.session_state.user_name,
        disabled=True
    )

    st.text_input(
        tr("phone"),
        value=st.session_state.phone,
        disabled=True
    )

    st.write(
        f"**{tr('preferred')}:** "
        f"{st.session_state.language}"
    )

    st.caption(tr("tagline"))

