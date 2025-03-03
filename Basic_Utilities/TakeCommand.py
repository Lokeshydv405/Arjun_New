import speech_recognition as sr
from Basic_Utilities.say import say
import eel
from mtranslate import translate

@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        query = translate_text(query)
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...",end='\n')
        eel.DisplayMessage("Say that again please...")
        eel.ShowHood()
        # say("Say that again please...")
        return None
    eel.DisplayMessage(query)
    eel.ShowHood()
    # say(query)
    return query


def translate_text(text, to_lang='en'):
    engligh_text =  translate(text, to_lang)
    return engligh_text

if __name__ == "__main__":
    sample_text = "how was the day? aaj din kaisa raha?"
    translated_text = translate_text(sample_text, 'en')
    print(f"Original text: {sample_text}")
    print(f"Translated text: {translated_text}")