import speech_recognition as sr

listener = sr.Recognizer()
#listener.dynamic_energy_threshold = False
def listen(t):
    try:
        with sr.Microphone() as source:
            print(f"[.......{t}.......]")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            print(command)
            return command
    except:
        if t>0:
            return listen(t-1)
        else:
            return None