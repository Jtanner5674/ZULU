import datetime
import webbrowser
import os
import sqlite3

# Time and Date Utilities
def current_time():
    time = datetime.datetime.now()
    return "The current time is " + time.strftime('%I:%M %p')

def current_date():
    date = datetime.datetime.now()
    return "Today's date is " + date.strftime('%A %B %d %Y')

# Browser-related commands
def open_browser(text):
    open_position = text.find('open')
    if open_position != -1:
        website_part = text[open_position + len('open'):].strip()
        domain_extensions = [".com", ".net", ".org", ".gov", ".edu"]
        for ext in domain_extensions:
            if ext in website_part:
                website_part = website_part.split(ext)[0] + ext
                break
        else:
            website_part += ".com"
        webbrowser.open("http://www." + website_part)
        return "Opening: " + website_part

def search_google(text):
    for_position = text.find('for')
    if for_position != -1:
        query = text[for_position + len('for'):].strip()
        webbrowser.open("https://www.google.com/search?q=" + query)
        return "Searching for " + query

# System commands
def system_command(command):
    if "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down system."
    elif "restart" in command:
        os.system("shutdown /r /t 1")
        return "Restarting system."
    else:
        return "Command not recognized."

# Stop Function
def exit_program():
    talk("Thank you for using Zulu! See you next time!")
    with sqlite3.connect('history.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM commands')
        conn.commit()
    exit()

# Repeat Last Command
def repeat():
    with sqlite3.connect('history.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM commands
            ORDER BY time DESC
            LIMIT 1
        ''')
        last_command = cursor.fetchone()
    if last_command:
        talk(f"Sure, I said: {last_command[1]}")
    else:
        talk("I have no recent commands to repeat.")
