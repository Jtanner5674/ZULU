import pyttsx3
import datetime
import sqlite3
import speech_recognition as sr

# Initialize speech engine
speechEngine = pyttsx3.init()
speechEngine.setProperty('volume', 1)
speechEngine.setProperty('rate', 150)

# Text-to-Speech function
def talk(string):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(string)
    with sqlite3.connect('history.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO commands (time, command) VALUES (?, ?)', (current_time, string))
        conn.commit()
    speechEngine.say(string)
    speechEngine.runAndWait()

# Listen for Speech
def audio_input():
    recognizer = sr.Recognizer()
    print("Say something:")
    with sr.Microphone() as source:
        sound = recognizer.listen(source)
    return sound

def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except sr.RequestError as error:
        return f"Error making request: {str(error)}"
