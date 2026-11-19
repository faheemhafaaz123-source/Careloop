import os
import json
import re
import sqlite3
import hashlib
import secrets
import hmac
import base64
from datetime import datetime, date
from io import BytesIO
import wave
import time

import streamlit as st
from google import genai
from google.genai import types

# ============================================================
# CARELOOP — complete single-file Streamlit application
# ============================================================

st.set_page_config(
    page_title="Careloop",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "careloop.db")
LOGO_PATH = os.path.join(BASE_DIR, "careloop_logo.jpeg")
LOGO_BASE64 = "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"

def display_careloop_logo(width):
    """Display the exact uploaded Careloop logo embedded in this app."""
    st.image(BytesIO(base64.b64decode(LOGO_BASE64)), width=width)
CHAT_MODEL = os.getenv("CARELOOP_GEMINI_MODEL", "gemini-3.5-flash-lite")
TTS_MODEL = os.getenv("CARELOOP_TTS_MODEL", "gemini-3.1-flash-tts-preview")
# Gemini handles text, transcription and spoken replies; no OpenAI client is used.

# 15 carefully selected language choices. English is the fallback language.
# Translations are cached in memory and SQLite after the first successful request.
# 100 language choices. English is the fallback language.
LANGUAGES = [
    'English',
    'Kannada',
    'Hindi',
    'Tamil',
    'Telugu',
    'Malayalam',
    'Bengali',
    'Marathi',
    'Gujarati',
    'Punjabi',
    'Urdu',
    'Odia',
    'Assamese',
    'Sanskrit',
    'Kashmiri',
    'Konkani',
    'Nepali',
    'Sindhi',
    'Dogri',
    'Maithili',
    'Arabic',
    'French',
    'Spanish',
    'German',
    'Japanese',
    'Chinese (Simplified)',
    'Chinese (Traditional)',
    'Portuguese',
    'Russian',
    'Italian',
    'Korean',
    'Turkish',
    'Persian',
    'Swahili',
    'Dutch',
    'Greek',
    'Hebrew',
    'Thai',
    'Vietnamese',
    'Indonesian',
    'Malay',
    'Filipino',
    'Burmese',
    'Khmer',
    'Lao',
    'Sinhala',
    'Ukrainian',
    'Polish',
    'Romanian',
    'Hungarian',
    'Czech',
    'Slovak',
    'Bulgarian',
    'Serbian',
    'Croatian',
    'Bosnian',
    'Macedonian',
    'Albanian',
    'Lithuanian',
    'Latvian',
    'Estonian',
    'Finnish',
    'Swedish',
    'Norwegian',
    'Danish',
    'Icelandic',
    'Irish',
    'Welsh',
    'Scottish Gaelic',
    'Basque',
    'Catalan',
    'Galician',
    'Afrikaans',
    'Amharic',
    'Somali',
    'Hausa',
    'Yoruba',
    'Igbo',
    'Zulu',
    'Xhosa',
    'Shona',
    'Kinyarwanda',
    'Malagasy',
    'Oromo',
    'Pashto',
    'Kurdish (Kurmanji)',
    'Kurdish (Sorani)',
    'Uzbek',
    'Kazakh',
    'Kyrgyz',
    'Tajik',
    'Turkmen',
    'Mongolian',
    'Georgian',
    'Armenian',
    'Azerbaijani',
    'Belarusian',
    'Haitian Creole',
    'Javanese',
    'Sundanese',
]
# Stable translation keys. Keep values in English; translation is generated
# once per language and stored in the translation_cache table.
UI_EN = {
    "app_tagline": "Your AI companion. Your everyday care.",
    "dashboard": "Dashboard",
    "companion": "AI Companion",
    "quiz": "Quick Quiz",
    "reminders": "Reminders",
    "profile": "Profile",
    "user_management": "User Management",
    "logout": "Log out",
    "welcome": "Your everyday care starts here.",
    "language": "App language",
    "login": "Log in",
    "register": "Create account",
    "email": "Email",
    "password": "Password",
    "name": "Your name",
    "password_hint": "Password (at least 8 characters)",
    "login_error": "Email or password is incorrect.",
    "register_success": "Account created. You can now log in.",
    "register_invalid": "Enter a name and a valid email address.",
    "register_password_short": "Use a password with at least 8 characters.",
    "duplicate_email": "An account with this email already exists.",
    "auth_intro_title": "A little support, whenever you need it.",
    "auth_intro": "Chat with your AI companion, practise with quick quizzes, and keep track of everyday reminders.",
    "voice_feature": "Voice input and spoken replies",
    "ai_feature": "AI-powered conversations",
    "reminder_feature": "Simple reminders",
    "medical_notice": "Careloop is an AI tool, not a medical or emergency service.",
    "choose_page": "Choose a page from the sidebar.",
    "chat_title": "Talk to your companion",
    "chat_caption": "AI-generated replies. Avoid sharing passwords, financial details, or highly sensitive personal information.",
    "message": "Type your message...",
    "send": "Send",
    "thinking": "Careloop is thinking...",
    "ai_error": "The AI request failed",
    "voice": "Speak to Careloop",
    "voice_help": "Allow microphone access when your browser asks.",
    "record": "Record a message",
    "transcribe_send": "Transcribe and send voice message",
    "listening": "Listening to your recording...",
    "no_speech": "No speech was detected. Try recording again.",
    "voice_error": "Voice transcription failed",
    "recognized": "Recognised speech",
    "read_reply": "Read the reply aloud",
    "generate_speech": "Generate spoken reply",
    "generating_voice": "Generating voice...",
    "speech_error": "Could not generate speech",
    "audio_note": "AI-generated voice. If your browser blocks autoplay, press Play.",
    "clear_chat": "Clear conversation",
    "quiz_topic": "Quiz topic",
    "quiz_topic_hint": "For example: healthy habits, science, English vocabulary",
    "difficulty": "Difficulty",
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
    "generate_quiz": "Generate quiz",
    "enter_topic": "Enter a topic first.",
    "creating_quiz": "Creating your quiz...",
    "quiz_error": "Could not create quiz",
    "choose_answer": "Choose one answer",
    "check_answers": "Check answers",
    "correct": "Correct",
    "correct_answer": "Correct answer",
    "score": "Score",
    "reminder_title": "Reminder",
    "date": "Date",
    "add_reminder": "Add reminder",
    "reminder_saved": "Reminder saved.",
    "enter_reminder": "Enter a reminder.",
    "delete": "Delete",
    "no_reminders": "No reminders yet.",
    "save_profile": "Save profile",
    "language_updated": "Language preference updated.",
    "total_users": "Total registered users",
    "registered_users": "Registered users",
    "registration_date": "Registration date",
    "not_available": "Not available",
    "no_users": "No users have registered yet.",
    "creator_access": "Creator access",
    "creator_code": "Creator access code",
    "enter_creator": "Enter as Creator",
    "wrong_creator_code": "Incorrect creator access code.",
    "creator_config_missing": "Creator access is not configured. Add the creator settings to Streamlit Secrets.",
    "creator_only": "This page is available only to the creator.",
    "hello": "Hello",
    "dashboard_companion": "Ask questions, think things through, or just talk.",
    "dashboard_quiz": "Generate a short learning or wellbeing quiz.",
    "dashboard_reminders": "Keep important tasks and dates in one place.",
    "difficulty_help": "Choose quiz difficulty",
    "delete_confirmed": "Reminder deleted.",
    "api_key_missing": "Gemini API key not found. Add GEMINI_API_KEY to Streamlit Secrets.",
    "translation_error": "Could not translate the interface. Showing English for now.",
    "translation_wait": "Preparing the selected language...",
    "profile_name": "Name",
    "profile_email": "Email",
    "creator_badge": "Creator",
    "logout_confirm": "You have been logged out.",
}

LANGUAGE_NATIVE = {
    "English": "English", "Kannada": "ಕನ್ನಡ", "Hindi": "हिन्दी",
    "Tamil": "தமிழ்", "Telugu": "తెలుగు", "Malayalam": "മലയാളം",
    "Bengali": "বাংলা", "Marathi": "मराठी", "Gujarati": "ગુજરાતી",
    "Punjabi": "ਪੰਜਾਬੀ", "Arabic": "العربية", "French": "Français",
    "Spanish": "Español", "German": "Deutsch", "Japanese": "日本語",
}


def db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT
            )
        """)
        # Upgrade older Careloop databases without deleting existing users.
        cols = {row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        for column, declaration in [
            ("name", "TEXT"),
            ("password_hash", "TEXT"),
            ("salt", "TEXT"),
            ("created_at", "TEXT"),
        ]:
            if column not in cols:
                conn.execute(f"ALTER TABLE users ADD COLUMN {column} {declaration}")
                cols.add(column)

        # Support older versions that used a `password` column.
        if "password" in cols:
            conn.execute("""
                UPDATE users SET password_hash = password
                WHERE (password_hash IS NULL OR password_hash = '')
                  AND password IS NOT NULL
            """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                title TEXT NOT NULL,
                reminder_date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        # Migrate older Careloop reminder tables safely. Earlier versions used
        # `due_date` instead of `reminder_date` and did not store `created_at`.
        # Keep the old columns and all existing rows; add the newer columns.
        reminder_cols = {
            row[1] for row in conn.execute("PRAGMA table_info(reminders)").fetchall()
        }
        if "reminder_date" not in reminder_cols:
            conn.execute("ALTER TABLE reminders ADD COLUMN reminder_date TEXT")
            reminder_cols.add("reminder_date")
        if "due_date" in reminder_cols:
            conn.execute("""
                UPDATE reminders
                SET reminder_date = due_date
                WHERE reminder_date IS NULL OR reminder_date = ''
            """)
        if "created_at" not in reminder_cols:
            conn.execute("ALTER TABLE reminders ADD COLUMN created_at TEXT")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS translation_cache (
                language TEXT PRIMARY KEY,
                translations_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 180000
    ).hex()


def create_user(name, email, password):
    email = email.strip().lower()
    salt = secrets.token_hex(16)
    hashed = hash_password(password, salt)
    with db() as conn:
        conn.execute("""
            INSERT INTO users(email, name, password_hash, salt, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (email, name.strip(), hashed, salt, datetime.now().isoformat()))


def authenticate(email, password):
    with db() as conn:
        row = conn.execute("""
            SELECT email, name, password_hash, salt
            FROM users WHERE email = ?
        """, (email.strip().lower(),)).fetchone()
    if not row or not row[2] or not row[3]:
        return None
    if hmac.compare_digest(hash_password(password, row[3]), row[2]):
        return {"email": row[0], "name": row[1]}
    return None


def get_client():
    """Create the Gemini client from Streamlit Secrets or an environment variable."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    key = key or os.getenv("GEMINI_API_KEY", "")
    return genai.Client(api_key=key) if key else None


def get_translation(client, language):
    """Translate the UI in small Gemini requests, retry temporary failures, and cache success."""
    if language == "English":
        return UI_EN

    cache_key = f"ui_translations_{language}"
    if cache_key in st.session_state:
        cached_session = st.session_state[cache_key]
        if isinstance(cached_session, dict) and all(k in cached_session for k in UI_EN):
            return cached_session
        st.session_state.pop(cache_key, None)

    # Reuse only complete cached translations. Ignore old/incomplete cache rows.
    try:
        with db() as conn:
            row = conn.execute(
                "SELECT translations_json FROM translation_cache WHERE language=?",
                (language,),
            ).fetchone()
        if row:
            cached = json.loads(row[0])
            if isinstance(cached, dict) and all(k in cached for k in UI_EN):
                translated = {key: str(cached[key]) for key in UI_EN}
                st.session_state[cache_key] = translated
                return translated
    except Exception:
        pass

    if client is None:
        st.error("Translation unavailable: GEMINI_API_KEY is not configured.")
        return UI_EN

    translated = {}
    items = list(UI_EN.items())
    delays = [2, 4, 8, 12]

    # Ten short strings per request helps avoid oversized responses.
    for start_index in range(0, len(items), 10):
        batch = dict(items[start_index:start_index + 10])
        prompt = (
            f"Translate every value in this JSON object into {language}. "
            "Preserve every key exactly. Return only a valid JSON object, no Markdown. "
            "Use short, natural wording suitable for app labels and buttons. "
            "Do not add, remove, or rename keys. Keep Careloop and AI unchanged. JSON:\n"
            + json.dumps(batch, ensure_ascii=False)
        )

        for attempt in range(4):
            try:
                response = client.models.generate_content(
                    model=CHAT_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=1200,
                        response_mime_type="application/json",
                    ),
                )
                raw = (response.text or "").strip()
                if not raw:
                    raise ValueError("Gemini returned an empty translation response.")
                raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                data = json.loads(raw)
                if not isinstance(data, dict) or not all(k in data for k in batch):
                    raise ValueError("Gemini returned incomplete translation JSON.")
                translated.update({key: str(data[key]) for key in batch})
                break
            except Exception as exc:
                message = str(exc).upper()
                temporary = any(token in message for token in (
                    "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED",
                    "500", "INTERNAL", "TIMEOUT", "DEADLINE"
                ))
                if temporary and attempt < 3:
                    time.sleep(delays[attempt])
                    continue
                st.error(
                    f"Translation failed for {language} ({type(exc).__name__}): {exc}"
                )
                return UI_EN

    # Save only after all batches have completed successfully.
    try:
        with db() as conn:
            conn.execute(
                """INSERT INTO translation_cache(language, translations_json, updated_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(language) DO UPDATE SET
                     translations_json=excluded.translations_json,
                     updated_at=excluded.updated_at""",
                (language, json.dumps(translated, ensure_ascii=False), datetime.now().isoformat()),
            )
    except Exception as exc:
        st.warning(f"Translation completed but could not be cached: {exc}")

    st.session_state[cache_key] = translated
    return translated


def tr(key):
    translations = st.session_state.get("ui_translations", UI_EN)
    return translations.get(key, UI_EN.get(key, key))


def ask_ai(client, messages, language, name):
    instructions = f"""
You are Careloop, a friendly, thoughtful everyday AI companion.
The user's name is {name}. Reply in {language}, unless the user clearly asks for another language.
Be warm but honest, practical, concise, and age-appropriate.
Do not claim to be a doctor, therapist, or emergency service. Do not diagnose.
For urgent danger or serious symptoms, tell the user to contact local emergency services
or a qualified professional. Do not invent facts. Never pretend to be human.
"""
    contents = []
    for item in messages:
        role = "model" if item.get("role") == "assistant" else "user"
        contents.append(types.Content(
            role=role,
            parts=[types.Part.from_text(text=str(item.get("content", "")))],
        ))
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=instructions,
            max_output_tokens=1200,
        ),
    )
    answer = (response.text or "").strip()
    if not answer:
        raise ValueError("Gemini returned an empty response.")
    return answer


def transcribe_audio(client, audio_file):
    """Transcribe a Streamlit audio recording using Gemini audio understanding."""
    audio_bytes = audio_file.getvalue()
    mime_type = getattr(audio_file, "type", None) or "audio/wav"
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=[
            types.Part.from_text(
                text="Transcribe the spoken words accurately. Return only the transcript."
            ),
            types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(max_output_tokens=1200),
    )
    return (response.text or "").strip()


def make_speech(client, text_to_speak):
    """Generate WAV audio with Gemini text-to-speech."""
    response = client.models.generate_content(
        model=TTS_MODEL,
        contents=f"Speak clearly and naturally. Match the language of this text: {text_to_speak[:4000]}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            ),
        ),
    )
    audio_data = response.candidates[0].content.parts[0].inline_data.data
    wav_buffer = BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_data)
    return wav_buffer.getvalue()


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: Inter, sans-serif; }
    .stApp { background: linear-gradient(135deg,#f7f5ff 0%,#f1f5ff 55%,#fff7fb 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#21124b,#3d287a); }
    [data-testid="stSidebar"] * { color: white !important; }
    .hero { padding:30px 32px; border-radius:24px; color:white;
      background:linear-gradient(120deg,#5b35b5,#7860df 58%,#9b77e8);
      box-shadow:0 12px 35px rgba(80,54,160,.18); margin-bottom:22px; }
    .hero h1 { color:white; font-size:2.15rem; margin:0 0 8px 0; }
    .hero p { color:#f2edff; font-size:1.03rem; margin:0; }
    .mini-card { background:rgba(255,255,255,.9); border:1px solid #e9e4fa;
      border-radius:18px; padding:20px; min-height:125px;
      box-shadow:0 5px 18px rgba(50,35,100,.05); }
    .mini-card h3 { margin:0 0 8px 0; color:#4b328e; }
    .mini-card p { margin:0; color:#665f78; }
    div.stButton > button { border-radius:12px; border:0; font-weight:650;
      background:linear-gradient(90deg,#6544c3,#8b69dc); color:white; padding:.58rem 1.1rem; }
    div.stButton > button:hover { color:white; border:0; filter:brightness(1.06); }
    </style>
    """, unsafe_allow_html=True)


def auth_screen(client):
    display_careloop_logo(250)
    st.markdown('<div class="hero"><p>Your AI companion. Your everyday care.</p></div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("## " + tr("auth_intro_title"))
        st.write(tr("auth_intro"))
        st.markdown(f"- 🌍 {len(LANGUAGES)} language options")
        st.markdown("- 🎙️ " + tr("voice_feature"))
        st.markdown("- 🧠 " + tr("ai_feature"))
        st.markdown("- 📅 " + tr("reminder_feature"))
        st.caption(tr("medical_notice"))

    with right:
        tab_login, tab_register = st.tabs([tr("login"), tr("register")])
        with tab_login:
            email = st.text_input(tr("email"), key="login_email")
            password = st.text_input(tr("password"), type="password", key="login_password")
            if st.button(tr("login"), use_container_width=True):
                user = authenticate(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.is_creator = False
                    st.rerun()
                else:
                    st.error(tr("login_error"))

        with tab_register:
            name = st.text_input(tr("name"), key="register_name")
            email_new = st.text_input(tr("email"), key="register_email")
            password_new = st.text_input(tr("password_hint"), type="password", key="register_password")
            if st.button(tr("register"), use_container_width=True):
                if not name.strip() or not email_new.strip() or "@" not in email_new:
                    st.error(tr("register_invalid"))
                elif len(password_new) < 8:
                    st.error(tr("register_password_short"))
                else:
                    try:
                        create_user(name, email_new, password_new)
                        st.success(tr("register_success"))
                    except sqlite3.IntegrityError:
                        st.error(tr("duplicate_email"))

    st.divider()
    st.subheader(tr("creator_access"))
    creator_code = st.text_input(tr("creator_code"), type="password", key="creator_access_code")
    if st.button(tr("enter_creator"), use_container_width=True):
        try:
            expected = st.secrets.get("CREATOR_ACCESS_CODE", "")
            creator_name = st.secrets.get("CREATOR_NAME", "Careloop Creator")
            creator_email = st.secrets.get("CREATOR_EMAIL", "creator@careloop.local")
        except Exception:
            expected = ""
            creator_name = "Careloop Creator"
            creator_email = "creator@careloop.local"

        if not expected:
            st.error(tr("creator_config_missing"))
        elif hmac.compare_digest(creator_code, str(expected)):
            st.session_state.user = {"name": creator_name, "email": creator_email}
            st.session_state.is_creator = True
            st.rerun()
        else:
            st.error(tr("wrong_creator_code"))


def dashboard():
    user = st.session_state.user
    st.markdown(f"""
    <div class="hero">
      <h1>{tr('hello')}, {user['name']} 👋</h1>
      <p>{tr('welcome')}</p>
    </div>
    """, unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown(f'<div class="mini-card"><h3>💬 {tr("companion")}</h3><p>{tr("dashboard_companion")}</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown(f'<div class="mini-card"><h3>🧠 {tr("quiz")}</h3><p>{tr("dashboard_quiz")}</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown(f'<div class="mini-card"><h3>📅 {tr("reminders")}</h3><p>{tr("dashboard_reminders")}</p></div>', unsafe_allow_html=True)
    st.write("")
    st.info(tr("choose_page"))


def companion_page(client):
    st.markdown("## 💬 " + tr("companion"))
    st.caption(tr("chat_caption"))
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_area(tr("message"), height=90, key="typed_prompt")
        sent = st.form_submit_button(tr("send"), use_container_width=True)

    if sent and prompt.strip():
        st.session_state.chat_history.append({"role": "user", "content": prompt.strip()})
        with st.spinner(tr("thinking")):
            try:
                answer = ask_ai(
                    client, st.session_state.chat_history,
                    st.session_state.language, st.session_state.user["name"]
                )
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.session_state.last_reply = answer
            except Exception as exc:
                st.error(f"{tr('ai_error')}: {exc}")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎙️ " + tr("voice"))
    st.caption(tr("voice_help"))
    recording = st.audio_input(tr("record"), sample_rate=16000, key="careloop_mic")
    if recording is not None and st.button(tr("transcribe_send"), key="send_voice"):
        with st.spinner(tr("listening")):
            try:
                transcript = transcribe_audio(client, recording)
                if not transcript:
                    st.warning(tr("no_speech"))
                else:
                    st.session_state.chat_history.append({"role": "user", "content": transcript})
                    answer = ask_ai(
                        client, st.session_state.chat_history,
                        st.session_state.language, st.session_state.user["name"]
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.session_state.last_reply = answer
                    st.session_state.voice_transcript = transcript
                    st.rerun()
            except Exception as exc:
                st.error(f"{tr('voice_error')}: {exc}")

    if st.session_state.get("voice_transcript"):
        st.info(f"{tr('recognized')}: {st.session_state.voice_transcript}")

    last_reply = st.session_state.get("last_reply")
    if last_reply:
        st.markdown("---")
        st.markdown("### 🔊 " + tr("read_reply"))
        if st.button(tr("generate_speech"), key="generate_speech"):
            with st.spinner(tr("generating_voice")):
                try:
                    st.session_state.reply_audio = make_speech(client, last_reply)
                except Exception as exc:
                    st.error(f"{tr('speech_error')}: {exc}")
        if st.session_state.get("reply_audio"):
            st.audio(st.session_state.reply_audio, format="audio/wav")
            st.caption(tr("audio_note"))

    if st.button(tr("clear_chat"), key="clear_chat"):
        for key in ["chat_history", "last_reply", "reply_audio", "voice_transcript"]:
            st.session_state.pop(key, None)
        st.rerun()


def generate_quiz_content_with_retry(client, prompt, max_attempts=4):
    """Call Gemini for quiz JSON, retrying temporary overload/rate failures."""
    delays = [2, 4, 8]
    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(
                model=CHAT_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=950,
                    response_mime_type="application/json",
                ),
            )
        except Exception as exc:
            message = str(exc).upper()
            is_temporary = (
                "503" in message
                or "UNAVAILABLE" in message
                or "429" in message
                or "RESOURCE_EXHAUSTED" in message
                or "500" in message
                or "INTERNAL" in message
            )
            if not is_temporary or attempt >= max_attempts - 1:
                raise
            wait_seconds = delays[min(attempt, len(delays) - 1)]
            time.sleep(wait_seconds)

    raise RuntimeError("Gemini could not generate the quiz after several attempts.")


def quiz_page(client):
    st.markdown("## 🧠 " + tr("quiz"))
    topic = st.text_input(tr("quiz_topic"), placeholder=tr("quiz_topic_hint"))
    difficulty_labels = [tr("easy"), tr("medium"), tr("hard")]
    difficulty = st.selectbox(tr("difficulty"), difficulty_labels)
    if st.button(tr("generate_quiz")):
        if not topic.strip():
            st.warning(tr("enter_topic"))
        else:
            prompt = f"""Create exactly 5 useful multiple-choice questions.
Topic: {topic}
Difficulty: {difficulty}
Language: {st.session_state.language}

Return ONLY a valid JSON array. Each item must contain:
- "question": a concise question
- "options": exactly 4 short, distinct answer strings
- "answer": the zero-based integer index of the one correct option
- "explanation": one short sentence explaining the answer

Avoid long introductions and unnecessary detail. Check that every answer index is correct.
Do not use Markdown fences or text outside the JSON array."""
            with st.spinner(tr("creating_quiz")):
                try:
                    response = generate_quiz_content_with_retry(client, prompt)
                    raw = (response.text or "").strip()
                    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                    # Gemini can occasionally add a trailing comma before } or ].
                    raw = re.sub(r",\s*([}\]])", r"\1", raw)
                    quiz_data = json.loads(raw)
                    if not isinstance(quiz_data, list) or len(quiz_data) != 5:
                        raise ValueError("The AI did not return exactly five questions.")
                    for item in quiz_data:
                        if (
                            not isinstance(item, dict)
                            or not isinstance(item.get("question"), str)
                            or not isinstance(item.get("options"), list)
                            or len(item["options"]) != 4
                            or not isinstance(item.get("answer"), int)
                            or item["answer"] not in range(4)
                            or not isinstance(item.get("explanation"), str)
                        ):
                            raise ValueError("The quiz response had an invalid question format.")
                    st.session_state.quiz = quiz_data
                    st.session_state.quiz_topic = topic
                except Exception as exc:
                    error_text = str(exc)
                    if "503" in error_text or "UNAVAILABLE" in error_text.upper():
                        st.error(
                            "Gemini is temporarily busy. Careloop retried automatically, "
                            "but the service is still unavailable. Please try again in a minute."
                        )
                    elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text.upper():
                        st.error(
                            "Gemini's request quota is temporarily exhausted. "
                            "Please wait before generating another quiz."
                        )
                    else:
                        st.error(f"{tr('quiz_error')}: {exc}")

    if st.session_state.get("quiz"):
        st.markdown(f"### {st.session_state.get('quiz_topic', tr('quiz'))}")
        with st.form("quiz_answers"):
            chosen = []
            for i, question in enumerate(st.session_state.quiz):
                st.write(f"**{i + 1}. {question['question']}**")
                chosen.append(st.radio(
                    tr("choose_answer"), question["options"],
                    key=f"quiz_{i}", index=None
                ))
            checked = st.form_submit_button(tr("check_answers"))
        if checked:
            score = 0
            for question, answer in zip(st.session_state.quiz, chosen):
                correct = question["options"][question["answer"]]
                if answer == correct:
                    score += 1
                    st.success(f"{tr('correct')} — {question['explanation']}")
                else:
                    st.error(f"{tr('correct_answer')}: {correct}. {question['explanation']}")
            st.markdown(f"## {tr('score')}: {score} / {len(st.session_state.quiz)}")


def reminders_page():
    st.markdown("## 📅 " + tr("reminders"))
    with st.form("reminder_form", clear_on_submit=True):
        title = st.text_input(tr("reminder_title"))
        reminder_date = st.date_input(tr("date"), value=date.today())
        added = st.form_submit_button(tr("add_reminder"))
    if added:
        if title.strip():
            with db() as conn:
                conn.execute("""
                    INSERT INTO reminders(email,title,reminder_date,created_at)
                    VALUES(?,?,?,?)
                """, (
                    st.session_state.user["email"], title.strip(),
                    reminder_date.isoformat(), datetime.now().isoformat()
                ))
            st.success(tr("reminder_saved"))
        else:
            st.warning(tr("enter_reminder"))

    with db() as conn:
        rows = conn.execute("""
            SELECT id,title,reminder_date FROM reminders
            WHERE email=? ORDER BY reminder_date ASC
        """, (st.session_state.user["email"],)).fetchall()

    if rows:
        for reminder_id, title, due in rows:
            col1, col2 = st.columns([5, 1])
            col1.write(f"**{title}** · {due}")
            if col2.button(tr("delete"), key=f"delete_{reminder_id}"):
                with db() as conn:
                    conn.execute(
                        "DELETE FROM reminders WHERE id=? AND email=?",
                        (reminder_id, st.session_state.user["email"])
                    )
                st.rerun()
    else:
        st.info(tr("no_reminders"))


def profile_page():
    st.markdown("## 👤 " + tr("profile"))
    user = st.session_state.user
    st.write(f"**{tr('profile_name')}:** {user['name']}")
    st.write(f"**{tr('profile_email')}:** {user['email']}")
    new_language = st.selectbox(
        tr("language"),
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language),
        key="profile_language",
        format_func=lambda item: f"{LANGUAGE_NATIVE.get(item, item)} — {item}",
    )
    if st.button(tr("save_profile")):
        st.session_state.language = new_language
        st.session_state.ui_translations = get_translation(
            st.session_state.client, new_language
        )
        st.success(tr("language_updated"))
        st.rerun()


def creator_users_page():
    if not st.session_state.get("is_creator", False):
        st.error(tr("creator_only"))
        return

    st.markdown("## 👥 " + tr("user_management"))
    with db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        rows = conn.execute("""
            SELECT name, email, created_at
            FROM users
            ORDER BY created_at DESC
        """).fetchall()

    st.metric(tr("total_users"), total)
    st.subheader(tr("registered_users"))
    if not rows:
        st.info(tr("no_users"))
        return

    table = []
    for name, email, created_at in rows:
        if created_at:
            try:
                created = datetime.fromisoformat(created_at).strftime("%d %b %Y, %I:%M %p")
            except ValueError:
                created = created_at
        else:
            created = tr("not_available")
        table.append({
            tr("name"): name or tr("not_available"),
            tr("email"): email,
            tr("registration_date"): created,
        })
    st.dataframe(table, use_container_width=True, hide_index=True)


def main():
    init_db()
    inject_css()

    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "user" not in st.session_state:
        st.session_state.user = None
    if "is_creator" not in st.session_state:
        st.session_state.is_creator = False

    client = get_client()
    st.session_state.client = client

    # Language selector is available before login.
    if not st.session_state.user:
        language_choice = st.selectbox(
            "🌐 " + UI_EN["language"],
            LANGUAGES,
            index=LANGUAGES.index(st.session_state.language),
            key="prelogin_language",
            format_func=lambda item: f"{LANGUAGE_NATIVE.get(item, item)} — {item}",
        )
        if language_choice != st.session_state.language:
            st.session_state.language = language_choice
            st.rerun()

    st.session_state.ui_translations = get_translation(
        client, st.session_state.language
    )

    if not st.session_state.user:
        auth_screen(client)
        return

    with st.sidebar:
        display_careloop_logo(165)
        st.caption(tr("app_tagline"))
        st.write(f"{tr('hello')}, {st.session_state.user['name']}")
        language_choice = st.selectbox(
            tr("language"),
            LANGUAGES,
            index=LANGUAGES.index(st.session_state.language),
            key="sidebar_language",
            format_func=lambda item: f"{LANGUAGE_NATIVE.get(item, item)} — {item}",
        )
        if language_choice != st.session_state.language:
            st.session_state.language = language_choice
            st.session_state.ui_translations = get_translation(client, language_choice)
            st.rerun()

        pages = [
            tr("dashboard"), tr("companion"), tr("quiz"),
            tr("reminders"), tr("profile"),
        ]
        if st.session_state.get("is_creator", False):
            pages.append(tr("user_management"))
        page = st.radio("Menu", pages, label_visibility="collapsed")

        if st.session_state.get("is_creator", False):
            st.caption("🔐 " + tr("creator_badge"))

        if st.button(tr("logout"), use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in ["language", "ui_translations"]:
                    st.session_state.pop(key, None)
            st.session_state.user = None
            st.session_state.is_creator = False
            st.rerun()

    if not client:
        st.error(tr("api_key_missing"))
        return

    if page == tr("dashboard"):
        dashboard()
    elif page == tr("companion"):
        companion_page(client)
    elif page == tr("quiz"):
        quiz_page(client)
    elif page == tr("reminders"):
        reminders_page()
    elif page == tr("profile"):
        profile_page()
    elif page == tr("user_management") and st.session_state.get("is_creator", False):
        creator_users_page()


if __name__ == "__main__":
    main()
