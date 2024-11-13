import pyttsx3
import datetime
import wikipedia

import speech_recognition as sr
import webbrowser
import os
import smtplib
import pyaudio
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am RJ, designed by Rahul. How can I assist you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    except sr.RequestError:
        print("Network issues. Please check your internet connection.")
        return "None"
    return query.lower()

def send_email(to, content):
    """Sends an email with the specified content."""
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('youremail@gmail.com', 'yourpassword')  
            server.sendmail('youremail@gmail.com', to, content)
            speak("The email has been sent.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("I'm sorry, I was unable to send the email at this moment.")

if __name__ == "__main__":
    speak("Hello Rahul, how are you?")
    wish_me()

    while True:
        query = take_command()

        if 'search' in query:
            speak('Searching Wikipedia...')
            query = query.replace("search", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for this search. Please specify further.")
            except wikipedia.exceptions.PageError:
                speak("No results found on Wikipedia.")

        elif 'open' in query:
            sites = {
                'youtube': 'https://youtube.com',
                'google': 'https://google.com',
                'cricbuzz': 'https://cricbuzz.com',
                'hackerrank': 'https://hackerrank.com',
                'hackingloops': 'https://hackingloops.com',
                'facebook': 'https://facebook.com',
                'whatsapp': 'https://web.whatsapp.com'
            }
            for site, url in sites.items():
                if site in query:
                    speak(f'Opening {site}')
                    webbrowser.open(url)

        elif 'play music' in query:
            music_dir = 'E:\\ritz'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music.")
            else:
                speak("No songs found in the directory.")

        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'open' in query:
            app_paths = {
                'notepad plus plus': "C:\\Program Files (x86)\\Notepad++\\notepad++.exe",
                'powerpoint': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\PowerPoint 2013",
                'excel': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Excel 2013",
                'access': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Access 2013",
                'word': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Word 2013"
            }
            for app, path in app_paths.items():
                if app in query and os.path.exists(path):
                    os.startfile(path)
                    speak(f"Opening {app}")

        elif 'send email to rahul' in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = 'receiveremail@gmail.com' 
                send_email(to, content)
            except Exception as e:
                print(e)
                speak("Unable to send email at this time.")

        elif 'who created you' in query:
            speak("I was created by Rahul.")

        elif 'bye' in query:
            speak("It was nice talking to you. Have a great day! Goodbye!")
            break
