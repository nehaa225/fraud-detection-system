# voice_detection.py
import speech_recognition as sr
import streamlit as st

def detect_voice_from_file(file):
    """
    Converts uploaded audio file to text using Google Speech Recognition
    """
    if not file:
        return "No file uploaded"
    
    r = sr.Recognizer()
    
    # Use AudioFile for uploaded file
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Could not understand audio"