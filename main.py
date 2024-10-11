from speech import talk, audio_input, recognize_speech
from utils import current_time, current_date, open_browser, search_google, system_command, exit_program, repeat
import spacy
import sqlite3

# Load spacy model
# Run in terminal: 'python -m spacy download en_core_web_sm' 
nlp = spacy.load('en_core_web_sm')

# Wakeword Class and Object
class WakeClass:
    def __init__(self):
        with open('wakeword.txt', 'r') as wakeword_file:
            wakeWord, wake = wakeword_file.readlines()[0].strip().split(',')
        self.wakeWord = wakeWord.lower()
        self.wakeToggle = eval(wake)

    def save(self):
        with open("wakeword.txt", "w") as wakeword_save:
            wakeword_save.write(f"{self.wakeWord},{self.wakeToggle}")

wake = WakeClass()

# Command Processing
def task(text):
    doc = nlp(text)
    
    if any([token.lemma_ == "time" for token in doc]):
        talk(current_time())
    elif any([token.lemma_ == "date" for token in doc]):
        talk(current_date())
    elif any([token.lemma_ == "open" for token in doc]):
        talk(open_browser(text))
    elif any([token.lemma_ == "search" for token in doc]):
        talk(search_google(text))
    elif any([token.lemma_ == "shut down" or token.lemma_ == "restart" for token in doc]):
        talk("Are you sure?")
        audio = audio_input()
        speech = recognize_speech(audio)
        if "yes" in speech:
            talk(system_command(text))
        else:
            talk("Cancelling")
    elif any([token.lemma_ == "repeat" for token in doc]):
        repeat()
    elif "quit" in text or "exit" in text or "halt" in text or "stop" in text or "close" in text:
        exit_program()
    else:
        talk("Unknown command. Please try again.")

# Main Loop
if __name__ == "__main__":
    while True:
        audio = audio_input()
        speech = recognize_speech(audio)
        if wake.wakeWord in speech:
            task(speech)
        elif not wake.wakeToggle:
            task(speech)
