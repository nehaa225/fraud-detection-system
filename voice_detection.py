import speech_recognition as sr

file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
if file:
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    text = r.recognize_google(audio)
    st.write("Detected Speech:", text)