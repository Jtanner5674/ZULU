## Please be sure to run in your terminal: 'python -m spacy download en_core_web_sm' before running this program

# Library and APIs and stuff
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import spacy

# Speech Recognition Object
recognizer = sr.Recognizer()

# Load spacy model
nlp = spacy.load('en_core_web_sm')

# Wakeword Class and Object
class WakeClass:
    with open('wakeword.txt', 'r') as wakeword_file:
        wakeword_settings = wakeword_file.readlines()
    wakeWord, wake = wakeword_settings[0].strip().split(',')
    wakeWord = wakeWord.lower()
    wakeToggle = eval(wake)
    wakeword_file.close()
    def save(self):
        wakeword_save = open("wakeword.txt", "w")
        wakeword_save.writelines([self.wakeWord, ",", str(self.wakeToggle)])
        wakeword_save.close()
wake = WakeClass()

# Text To Speech
speechEngine = pyttsx3.init()
speechEngine.setProperty('volume', 1)
speechEngine.setProperty('rate', 150)
def talk(string):
    print(string)
    speechEngine.say(string)
    speechEngine.runAndWait()

# Listen for Speech
def audio_input():
    print("Say something:")
    with sr.Microphone() as source:
        sound = recognizer.listen(source)
    return sound

# Current Time
def current_time():
   time = datetime.datetime.now()
   time_string = "The current time is " + time.strftime('%I:%M %p')
   talk(time_string)
 
# Current Date
def current_date():
   date = datetime.datetime.now()
   date_string = "Today's date is " + date.strftime('%A %B %d %Y')
   talk(date_string)

# Opens Websites
def open_browser(text):
    # Find the position of the word "open"
    open_position = text.find('open')
    if open_position != -1:
        # Extract the part of the text after "open"
        website_part = text[open_position + len('open'):].strip()
        
        # Check for domain extensions
        domain_extensions = [".com", ".net", ".org", ".gov", ".edu"]
        extension_found = False

        for ext in domain_extensions:
            if ext in website_part:
                # Slice the website part to remove anything after the extension
                website_part = website_part.split(ext)[0] + ext
                extension_found = True
                break  # Exit once we find the first valid extension

        # If no extension was found, default to .com
        if not extension_found:
            website_part += ".com"

        # Open the website
        webbrowser.open("http://www." + website_part)
        talk("Opening: " + website_part)
    
# Searches Google
def search_google(text):
    for_position = text.find('for')
    if for_position != -1:
        # Extract the part of the text after "for" like web search does "open"
        text = text[for_position + len('for'):].strip()
    webbrowser.open("https://www.google.com/search?q=" + text)
    talk("Searching for" + text)

# Stop Function
def stop():
    talk("Thank you for using Zulu! See you next time!")
    exit()

# Halt Function
def halt():
    talk("Bye")
    exit()
    
    
valid_commands = ["current time", "today's date", "open", "search for", "quit", "halt"]
# AI
def task(text):
    doc = nlp(text)
    for token in doc:
        print(token.text, token.pos_, token.dep_)

    # Extract intents from the parsed text
    if any([token.lemma_ == "time" for token in doc]):
        current_time()
    elif any([token.lemma_ == "date" for token in doc]):
        current_date()
    elif any([token.lemma_ == "open" for token in doc]):
        open_browser(text)
    elif any([token.lemma_ == "search" for token in doc]):
        search_google(text)
    elif "quit" in text or "exit" in text:
        stop()
    elif "halt" in text or "stop" in text:
        halt()
    else:
        talk("Unknown command. Please try again.")

# AI Loop
while True:
    audio = audio_input()
    try:
        speech = recognizer.recognize_google(audio)
        print("You said: " + speech)
        speech = speech.lower()
        if wake.wakeWord in speech:
            speech = speech[(speech.rfind(wake.wakeWord) + len(wake.wakeWord) + 1):]
            print("Executing")
            task(speech)
        elif not wake.wakeToggle:
            task(speech)
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as error:
        talk("Error making request to Google Speech Recognition service: " + str(error))
