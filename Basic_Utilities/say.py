import pyttsx3
# from  ..Settings.speaking import selected_voice
def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_id = []
    for voice in voices:
        # print(voice.id)
        voice_id.append(voice.id)
        
    engine.setProperty('voice', voice_id[0])
    engine.say(text)
    engine.runAndWait()
    engine.stop()
        
if __name__ == "__main__":
    say("Hello World")