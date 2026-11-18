import os
import json
import sqlite3
import hashlib
import secrets
import hmac
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
CHAT_MODEL = os.getenv("CARELOOP_GEMINI_MODEL", "gemini-3.5-flash-lite")
TTS_MODEL = os.getenv("CARELOOP_TTS_MODEL", "gemini-3.1-flash-tts-preview")
# Gemini handles text, transcription and spoken replies; no OpenAI client is used.

# 15 carefully selected language choices. English is the fallback language.
# Translations are cached in memory and SQLite after the first successful request.
LANGUAGES = [
    "English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam",
    "Bengali", "Marathi", "Gujarati", "Punjabi", "Arabic",
    "French", "Spanish", "German", "Japanese",
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
    """Load a cached translation first; call the configured model only on a cache miss."""
    if language == "English":
        return UI_EN

    cache_key = f"ui_translations_{language}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    # Existing translations from the earlier Careloop version are reused.
    try:
        with db() as conn:
            row = conn.execute(
                "SELECT translations_json FROM translation_cache WHERE language=?",
                (language,),
            ).fetchone()
        if row:
            cached = json.loads(row[0])
            if isinstance(cached, dict) and cached:
                translated = {
                    key: str(cached.get(key, value))
                    for key, value in UI_EN.items()
                }
                st.session_state[cache_key] = translated
                return translated
    except Exception:
        # A missing or damaged cache should not prevent a fresh translation.
        pass

    if client is None:
        st.error("Translation unavailable: GEMINI_API_KEY is not configured.")
        return UI_EN

    prompt = (
        f"Translate every value in this JSON object into {language}. "
        "Preserve every key exactly. Return only one valid JSON object, with no markdown. "
        "Use short, natural wording for app buttons, labels and messages. "
        "Keep Careloop and AI unchanged where appropriate. Do not add or remove keys. JSON:\n"
        + json.dumps(UI_EN, ensure_ascii=False)
    )

    try:
        response = client.models.generate_content(
            model=CHAT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=2600),
        )
        raw = (response.text or "").strip()
        if raw.startswith("```json"):
            raw = raw[len("```json"):]
        elif raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        translated_data = json.loads(raw.strip())
        if not isinstance(translated_data, dict):
            raise ValueError("The translation response was not a JSON object.")

        translated = {
            key: str(translated_data.get(key, value))
            for key, value in UI_EN.items()
        }

        # Save once. Next language selection reads from session or SQLite,
        # so it does not need another translation API request.
        with db() as conn:
            conn.execute(
                """INSERT INTO translation_cache(language, translations_json, updated_at)
                   VALUES (?, ?, ?)
                   ON CONFLICT(language) DO UPDATE SET
                     translations_json=excluded.translations_json,
                     updated_at=excluded.updated_at""",
                (language, json.dumps(translated, ensure_ascii=False), datetime.now().isoformat()),
            )

        st.session_state[cache_key] = translated
        return translated

    except Exception as exc:
        # Show the actual API error so model access, quota and key problems
        # can be distinguished instead of silently pretending translation ran.
        st.error(f"Translation failed ({type(exc).__name__}): {exc}")
        return UI_EN


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
    st.markdown("""
    <div class="hero">
      <h1>💜 Careloop</h1>
      <p>Your AI companion. Your everyday care.</p>
    </div>
    """, unsafe_allow_html=True)
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
        st.markdown("# 💜 Careloop")
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
