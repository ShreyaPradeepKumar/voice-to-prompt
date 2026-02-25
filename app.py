import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Voice to Prompt Converter",
    page_icon="🎙️",
    layout="centered"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY not found in environment variables!")
        st.info("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_openai_client()

def improve_prompt(text):
    """Convert raw user input into a clear, structured, professional prompt."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You convert raw user requests into clear, structured, professional prompts.
                    
Rules:
- Rewrite clearly
- Add necessary context
- Make it specific
- Make it AI-ready
- Do NOT add extra explanation
Return only the improved prompt."""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error improving prompt: {e}")
        return text

# App title and description
st.title("🎙️ Voice to Prompt Converter")
st.markdown("**Speak in English or Hindi** - Get an AI-ready prompt!")
st.divider()

# Initialize session state
if 'recognized_text' not in st.session_state:
    st.session_state.recognized_text = None
if 'english_text' not in st.session_state:
    st.session_state.english_text = None
if 'final_prompt' not in st.session_state:
    st.session_state.final_prompt = None
if 'detected_language' not in st.session_state:
    st.session_state.detected_language = None

# Settings
col1, col2 = st.columns(2)
with col1:
    duration = st.slider("🕐 Recording Duration (seconds)", 3, 15, 8)
with col2:
    language_option = st.selectbox(
        "🌍 Language Detection",
        ["Auto (English/Hindi)", "English Only", "Hindi Only"]
    )

st.divider()

# Record button
if st.button("🎙️ Start Recording", type="primary", use_container_width=True):
    r = sr.Recognizer()
    
    with st.spinner("🔧 Initializing microphone..."):
        try:
            with sr.Microphone() as source:
                st.info("🎤 **Listening... Speak now!**")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.record(source, duration=duration)
            
            with st.spinner("🔄 Processing your speech..."):
                # Determine language based on selection
                if language_option == "English Only":
                    languages = [("en-IN", "English")]
                elif language_option == "Hindi Only":
                    languages = [("hi-IN", "Hindi")]
                else:
                    languages = [("en-IN", "English"), ("hi-IN", "Hindi")]
                
                # Try recognizing in selected language(s)
                recognized = False
                for lang_code, lang_name in languages:
                    try:
                        text = r.recognize_google(audio, language=lang_code)
                        st.session_state.recognized_text = text
                        st.session_state.detected_language = lang_name
                        recognized = True
                        break
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        st.error(f"❌ Speech recognition service error: {e}")
                        st.stop()
                
                if not recognized:
                    st.error("❌ Could not understand audio. Please speak clearly and try again.")
                    st.stop()
                
                # Translate to English if needed
                st.session_state.english_text = GoogleTranslator(
                    source="auto", 
                    target="en"
                ).translate(st.session_state.recognized_text)
                
                # Improve prompt using OpenAI
                st.session_state.final_prompt = improve_prompt(st.session_state.english_text)
                
            st.success("✅ Processing complete!")
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Make sure your microphone is connected and permissions are granted.")

# Display results
if st.session_state.recognized_text:
    st.divider()
    
    # Original text
    st.subheader(f"📝 Original Text ({st.session_state.detected_language})")
    st.info(st.session_state.recognized_text)
    
    # Translated text (if different from original)
    if st.session_state.detected_language == "Hindi":
        st.subheader("🌍 Translated to English")
        st.info(st.session_state.english_text)
    
    # AI-improved prompt
    st.subheader("✨ AI-Ready Prompt")
    st.success(st.session_state.final_prompt)
    
    # Copy button
    st.code(st.session_state.final_prompt, language=None)
    
    # Reset button
    if st.button("🔄 Record Again", use_container_width=True):
        st.session_state.recognized_text = None
        st.session_state.english_text = None
        st.session_state.final_prompt = None
        st.session_state.detected_language = None
        st.rerun()

# Footer
st.divider()
st.caption("💡 Tip: Speak clearly in a quiet environment for best results.")