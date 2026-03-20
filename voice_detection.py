# voice_detection.py
import speech_recognition as sr

def detect_voice_from_file(file):
    """
    Convert uploaded audio file (wav/mp3) to text using Google Speech Recognition
    """
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Could not understand audio"