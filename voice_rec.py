import speech_recognition as sr

def recognize_cmd(timeout=10):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source) #helps filter out background noise
            print("Listening...")
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio).lower()
        except:
            sr.UnknownValueError
            return "I'm sorry, I could not understand."
    return command