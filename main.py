# Library and APIs and stuff
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import googleapiclient.discovery
import cv2
import face_recognition
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from pynput import mouse
import pyautogui
import threading
import time
import wikipedia
import re

# Speech Recognition Object
recognizer = sr.Recognizer()
muted = False
test =  True

# Other API Information
api_key = "AIzaSyCmz1hqVoMDqCy6UDKQf6G7UtV4srIwwoE"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)


#GUI Setup
def gui():
   win = Tk()
   # Set the geometry of Tkinter Frame
   win.geometry("1024x600")
   # Open the Image File
   bg = ImageTk.PhotoImage(file="background.png")
   # Create a Canvas
   canvas = Canvas(win, width=700, height=3500)
   canvas.pack(fill=BOTH, expand=True)
   # Add Image inside the Canvas
   canvas.create_image(0, 0, image=bg, anchor='nw')
   # Define a global variable


   # Create a function to change the global variable
   def change_var():
       global muted
       muted = not muted
       print(muted)
   # Create a button
   button = Button(win, text="Mute", command=change_var)
   # Place the button at a specific location in the window
   button.place(x=100, y=100, width=100, height=50)


   # Function to resize the window
   # noinspection PyUnresolvedReferences
   def resize_image(e):
       global image, resized, image2
       # open image to resize it
       image = Image.open("background.png")
       # resize the image with width and height of root
       resized = image.resize((e.width, e.height), Image.Resampling.LANCZOS)
       image2 = ImageTk.PhotoImage(resized)
       canvas.create_image(0, 0, image=image2, anchor='nw')
   def move_mouse_and_click():
       # Get the screen width and height
       screen_width, screen_height = pyautogui.size()


       # Calculate the coordinates of the top middle of the screen
       x = screen_width // 2
       y = 0


       # Move the mouse to the top middle of the screen
       mouse.Controller().position = (x, y)


       # Click the mouse
       mouse.Controller().press(mouse.Button.left)
       mouse.Controller().release(mouse.Button.left)


   # Set the window to fullscreen
   win.state("zoomed")
   # Bind the function to configure the parent window
   win.bind("<Configure>", resize_image)
   win.after(1, move_mouse_and_click)
   win.mainloop()
thread = threading.Thread(target=gui)
thread.start()




# Wakeword Class and Object
class wakeClass:
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

wake = wakeClass()

# Text To Speech
speechEngine = pyttsx3.init()
speechEngine.setProperty('volume', 1)
speechEngine.setProperty('rate', 150)

# Camera setup
def lookingGlass():
   video_capture = cv2.VideoCapture(0)
   known_face_encodings = []
   with open("names.txt", "r") as file:
       lines = file.readlines()
       lines = [line.strip() for line in lines]
       known_face_names = lines
       face_locations = []
       face_encodings = []
       face_names = []
       process_this_frame = True
   # Create an empty dictionary
   images = {}


   # Open the text file in read mode
   with open("names.txt", "r") as file:
       # Iterate over the lines of the text file
       for line in file:
           # Split the line on the comma character
           names = line.strip().split(",")
           # Iterate over the names in the line
           for name in names:
               # Load the image for the element
               image = face_recognition.load_image_file(f"faces/{name}.jpg")
               # Add the image and name to the dictionary
               images[name] = image


   # Set up variables
   known_face_encodings = []
   known_face_names = []


   # Iterate over the keys and values in the images dictionary
   for name, image in images.items():
       # Get the face encoding for the element
       encoding = face_recognition.face_encodings(image)[0]
       # Append the encoding to the known_face_encodings list
       known_face_encodings.append(encoding)
       # Append the name to the known_face_names list
       known_face_names.append(name)


   while True:
       # Grab a single frame of video
       ret, frame = video_capture.read()


       # Only process every other frame of video to save time
       if process_this_frame:
           # Resize frame of video to 1/4 size for faster face recognition processing
           small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


           # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
           rgb_small_frame = small_frame[:, :, ::-1]


           # Find all the faces and face encodings in the current frame of video
           face_locations = face_recognition.face_locations(rgb_small_frame)
           face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


           face_names = []
           for face_encoding in face_encodings:
               # See if the face is a match for the known face(s)
               matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
               name = "Unknown"


               # # If a match was found in known_face_encodings, just use the first one.
               # if True in matches:
               #     first_match_index = matches.index(True)
               #     name = known_face_names[first_match_index]
               # Or instead, use the known face with the smallest distance to the new face
               face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
               best_match_index = np.argmin(face_distances)
               if matches[best_match_index]:
                   name = known_face_names[best_match_index]
               face_names.append(name)
       process_this_frame = not process_this_frame
       # Display the results
       for (top, right, bottom, left), name in zip(face_locations, face_names):
           # Scale back up face locations since the frame we detected in was scaled to 1/4 size
           top *= 4
           right *= 4
           bottom *= 4
           left *= 4


           # Draw a box around the face
           cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


           # Draw a label with a name below the face
           cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
           font = cv2.FONT_HERSHEY_DUPLEX
           cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


       # Display the resulting image
       cv2.imshow('Video', frame)


       # Hit 'q' on the keyboard to quit!
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break


   # Release handle to the webcam
   video_capture.release()
   cv2.destroyAllWindows()




def saveFace():
   camera = cv2.VideoCapture(0)
   _, frame = camera.read()
   image = frame
   print("Person Recognized, what is your name?")
   speechEngine.say("Person Recognized, what is your name?")
   speechEngine.runAndWait()
   sname = input("name:")
   speechEngine.say("You said " + sname + " correct?")
   speechEngine.runAndWait()
   response = input("y/n")
   response = response.lower()
   print(response)
   if 'y' in response:
       cv2.imwrite("faces/{}.jpg".format(sname), image)
       with open("names.txt", "a") as file:
           # Write the new line to the text file
           file.write(f",{sname}")
           speechEngine.say("Person save success")
           speechEngine.runAndWait()
   elif 'n' in response:
       speechEngine.say("Alright, lets try that again. What is your name?")
       speechEngine.runAndWait()
       sname = input("name:")
       speechEngine.say("You said " + sname + " correct?")
       speechEngine.runAndWait()
       response = input("y/n")
       response = response.lower()
       if 'y' in response:
           cv2.imwrite("faces/{}.jpg".format(sname), image)
           # Open the text file in append mode
           with open("names.txt", "a") as file:
               file.write(f",{sname}")
               speechEngine.say("Person save success")
               speechEngine.runAndWait()
       else:
           speechEngine.say("Person save failed, please try saving them again")
           speechEngine.runAndWait()
   else:
       speechEngine.say("Unable to save user due to invalid response, please reattempt save.")
       speechEngine.runAndWait()


def talk(string):
   print(string)
   speechEngine.say(string)
   speechEngine.runAndWait()




# Listen for Speech
def audioInput():
   print("Say something:")
   with sr.Microphone() as source:
       sound = recognizer.listen(source)
   return sound




# Current Time
def currentTime():
   time = datetime.datetime.now()
   timeString = "The current time is " + time.strftime('%I:%M %p')
   talk(timeString)




# Current Date
def currentDate():
   date = datetime.datetime.now()
   dateString = "Today's date is " + date.strftime('%A %B %d %Y')
   talk(dateString)




# Opens websites
def openBrowser(text):
   if text == "eclass":
       webbrowser.open(f"https://publish.gwinnett.k12.ga.us/gcps/home/gcpslogin?error=&username=")
       talk("Opening Eclass!")
   else:
       webbrowser.open(f"www.{text[5:]}.com")
       talk("Opening: " + text + ".com")


       # Halt Function

def automatic_wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        talk(f"Here's what I found on Wikipedia: {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        talk(f"I found multiple results for that search. You may want to be more specific. Options include: {', '.join(e.options[:3])}")
    except wikipedia.exceptions.PageError:
        talk("I'm sorry, I couldn't find any information on that topic.")
    except Exception as e:
        talk(f"An error occurred while searching on Wikipedia: {e}")


def halt():
   talk("Bye")
   exit()


def doMath(text):
    # use regular expressions to extract the math expression from the text
    expression = re.search('\d+(\s*[\+\-\*\/\^]\s*\d+)+', text)
    if expression:
        expression = expression.group()
        # replace the ^ operator with ** for performing power operation
        expression = expression.replace('^', '**')
        # evaluate the math expression using the `eval()` function
        result = eval(expression)
        talk("The result is " + str(result))
    else:
        talk("Sorry, I couldn't find a math expression in that. Please try again with a valid expression.")

# Stop Function
def stop():
   talk("Goodbye, see you next time!")
   exit()




# AI
def task(text):
   if 'time' in text:
       currentTime()
   elif "date" in text or 'day' in text:
       currentDate()
   elif 'looking at' in text:
       lookingGlass()
   elif any([True for e in ['+', '-', '*', '/', '^'] if e in text]) and any([True for e in text if e.isdigit()]):
     doMath(text)

   elif 'who' in text or 'what' in text:
       query = text
       automatic_wikipedia_search(query)
   elif 'open eclass' in text:
       openBrowser("eclass")
   elif text.startswith("search youtube for "):
       query = text[19:]
       print(query)
       request = youtube.search().list(part="id,snippet", type='video', q=query, maxResults=1)
       response = request.execute()
       video_id = response["items"][0]["id"]["videoId"]
       video_url = f"https://www.youtube.com/watch?v={video_id}"
       webbrowser.open(video_url)
       speechEngine.say("Searching youtube for" + text[18:])
       speechEngine.runAndWait()
   elif 'open' in text:
       openBrowser(text)
   elif 'search for' in text:
       webbrowser.open(f"https://www.google.com/search?q={text[10:]}")
       print("Searching for" + text[10:])
       speechEngine.say("Searching for" + text[10:])
       speechEngine.runAndWait()
   elif 'save face' in text:
       saveFace()
   else:
       talk("Unknown Command.")  # maybe add list of commands??




# AI Loop
while True:
    if not test:
           if not muted:
               audio = audioInput()
               try:
                   speech = recognizer.recognize_google(audio)
                   print("You said: " + speech)
                   speech = speech.lower()
                   speech = speech[(speech.rfind(wake.wakeWord) + len(wake.wakeWord) + 1):]
                   if wake.wakeWord in speech:
                       task(speech)
                   elif wake.wakeToggle == False:
                       task(speech)
               except sr.UnknownValueError:
                   talk("Sorry, I didn't understand that.")
               except sr.RequestError as error:
                   # noinspection PyTypeChecker
                   talk("Error making request to Google Speech Recognition service: " + error)
           else:
               time.sleep(1)
    else:
        task(input("what is your command?"))