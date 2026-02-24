import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator

st.title("Voice to Prompt")

r = sr.Recognizer()

if st.button("🎙️ Record"):
    with sr.Microphone() as source:
        st.write("Listening... Speak now")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.record(source, duration=8)

    try:
        text = r.recognize_google(audio)
        st.subheader("Original")
        st.write(text)

        translated = GoogleTranslator(source="auto", target="en").translate(text)
        st.subheader("Translated")
        st.write(translated)

    except:
        st.error("Could not understand audio")