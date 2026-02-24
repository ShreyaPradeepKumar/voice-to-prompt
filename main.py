from googletrans import Translator
import speech_recognition as sr

translator = Translator()
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("Original:", text)

    translated = translator.translate(text, dest='en')
    print("English:", translated.text)

except Exception as e:
    print("Error:", e)