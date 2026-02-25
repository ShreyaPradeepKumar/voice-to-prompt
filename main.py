import speech_recognition as sr
from deep_translator import GoogleTranslator
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️  ERROR: OPENAI_API_KEY not found in environment variables")
    print("Please create a .env file with your API key:")
    print("OPENAI_API_KEY=your_api_key_here")
    exit(1)

client = OpenAI(api_key=api_key)
r = sr.Recognizer()
r.pause_threshold = 1.5


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
        print(f"Error improving prompt: {e}")
        return text


def main():
    """Main function to capture voice and convert to prompt."""
    print("=" * 60)
    print("🎙️  VOICE TO PROMPT CONVERTER")
    print("Supports: English & Hindi")
    print("=" * 60)
    
    with sr.Microphone() as source:
        print("\n🔧 Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=2)

        print("🎤 Speak now (in English or Hindi)...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("❌ No speech detected. Please try again.")
            return

    print("🔄 Processing your speech...")
    
    try:
        # Try English first
        detected_lang = "en-IN"
        try:
            text = r.recognize_google(audio, language="en-IN")
            print(f"✅ Detected language: English")
        except:
            # Try Hindi if English fails
            detected_lang = "hi-IN"
            text = r.recognize_google(audio, language="hi-IN")
            print(f"✅ Detected language: Hindi")

        print(f"\n📝 Original Text ({detected_lang}):")
        print(f"   {text}")

        # Translate to English if needed
        english_text = GoogleTranslator(source="auto", target="en").translate(text)
        
        if detected_lang == "hi-IN":
            print(f"\n🌍 Translated to English:")
            print(f"   {english_text}")

        # Improve into AI-ready prompt
        print("\n🤖 Generating AI-ready prompt...")
        final_prompt = improve_prompt(english_text)

        print("\n" + "=" * 60)
        print("✨ AI-READY PROMPT:")
        print("=" * 60)
        print(final_prompt)
        print("=" * 60)

    except sr.UnknownValueError:
        print("❌ Could not understand audio. Please speak clearly and try again.")
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()