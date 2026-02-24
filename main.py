import speech_recognition as sr
from deep_translator import GoogleTranslator

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak (you have 8 seconds)...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.record(source, duration=8)  # ⬅️ fixed recording

try:
    text = r.recognize_google(audio)
    print("Original:", text)

    translated = GoogleTranslator(source="auto", target="en").translate(text)
    print("Translated:", translated)

except sr.UnknownValueError:
    print("Error: Could not understand audio")
except sr.RequestError as e:
    print("Error:", e)