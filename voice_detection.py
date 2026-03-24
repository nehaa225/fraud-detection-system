import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def detect_voice_from_file(uploaded_file):
    recognizer = sr.Recognizer()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Convert to WAV
    audio = AudioSegment.from_file(tmp_path)
    wav_path = tmp_path + ".wav"
    audio.export(wav_path, format="wav")

    # Read WAV file
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    # Convert speech to text
    try:
        text = recognizer.recognize_google(audio_data)
    except:
        text = "Could not understand audio"

    return text