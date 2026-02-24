import speech_recognition as sr
from deep_translator import GoogleTranslator

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Adjusting for noise...")
    recognizer.adjust_for_ambient_noise(source)

    print("Speak now...")
    audio = recognizer.listen(
        source,
        timeout=None,
        phrase_time_limit=None
    )
try:
    text = r.recognize_google(audio)
    print("Original:", text)

    translated = GoogleTranslator(source="auto", target="en").translate(text)
    print("Translated:", translated)

except sr.UnknownValueError:
    print("Error: Could not understand audio")
except sr.RequestError as e:
    print("Error:", e)