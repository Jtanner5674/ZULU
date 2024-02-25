## Good Zulu

# Library and APIs and stuff
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

# Speech Recognition Object
recognizer = sr.Recognizer()

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
    if ".com" in text:
        webbrowser.open("www." + text)
        talk("Opening: " + text)
    else:
        webbrowser.open("www." + text + ".com")
        talk("Opening: " + text + ".com")

# Searches Google For
def search_google(text):
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

# AI
def task(text):
    if 'current time' in text:
        current_time()
    elif "today's date" in text:
        current_date()
    elif 'open' in text:
        open_browser(text[5:])
    elif 'search for' in text:
        search_google(text[10:])
    elif 'quit' in text:
        stop()
    elif text == "halt":
        halt()
    else:
        talk("Unknown Command.") # maybe add list of commands??

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
