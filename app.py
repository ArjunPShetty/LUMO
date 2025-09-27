import speech_recognition as sr
import datetime
import webbrowser
import sys
import pywhatkit
import pyttsx3
import os
import subprocess
import psutil
import pyautogui

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

APP_NAME = "LUMO"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"[{APP_NAME}] Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"[{APP_NAME}] You said: {query}")
            return query.lower()
    except Exception:
        print(f"[{APP_NAME}] Voice not working. Please type your command below:")
        return input(f"{APP_NAME} Command: ").lower()

def show_help():
    commands = f"""
    === {APP_NAME} - Available Commands ===
    1. time                    - Get current time
    2. open youtube            - Open YouTube
    3. open google             - Open Google
    4. play <song>             - Play song on YouTube
    5. search <query>          - Google search
    6. open notepad/calculator/chrome - Open apps
    7. shutdown / restart / logout    - System control
    8. screenshot              - Take screenshot
    9. mute                    - Mute system volume
    10. battery                - Show battery percentage
    11. take a note            - Save a note
    12. read notes             - Read saved notes
    13. voice male/female      - Change assistant voice
    14. help                   - Show this help menu
    15. exit / quit            - Exit assistant
  
    """
    print(commands)
    speak("I have shown the list of commands on your screen.")

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak(f"I am your AI Assistant {APP_NAME}. How can I help you?")

def run_ai():
    wish_me()
    while True:
        query = take_command().strip()

        if not query:
            continue


        if "time" in query:  # Basic Commands
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(f"[{APP_NAME}] Time: {strTime}")

        elif query.startswith("open "):
            app = query.replace("open ", "").strip()

            if app == "notepad":
                os.startfile("notepad.exe")
                speak("Opening Notepad")
            elif app == "calculator":
                os.startfile("calc.exe")
                speak("Opening Calculator")
            elif app == "chrome":
                os.startfile("chrome.exe")
                speak("Opening Chrome")
            else:
                speak(f"Opening {app}")
                webbrowser.open(f"https://{app}.com")

        elif query.startswith("play "):
            song = query.replace("play ", "", 1).strip()
            if not song:
                speak("Which song should I play?")
                song = take_command()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif query.startswith("search "):
            search_query = query.replace("search ", "", 1).strip()
            if not search_query:
                speak("What do you want me to search?")
                search_query = take_command()
            speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "shutdown" in query:        # System Controls
            speak("Shutting down your computer.")
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            speak("Restarting your computer.")
            os.system("shutdown /r /t 1")

        elif "logout" in query:
            speak("Logging out now.")
            os.system("shutdown -l")

        elif "screenshot" in query:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot taken and saved as screenshot.png")

        elif "mute" in query:
            os.system("nircmd.exe mutesysvolume 1")  # requires NirCmd tool installed
            speak("System volume muted")

        elif "battery" in query:
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
            speak(f"Battery is at {percent} percent and it is {plugged}")
            print(f"[{APP_NAME}] Battery: {percent}% ({plugged})")

        elif "take a note" in query:  # Notes Feature
            speak("What should I write in your note?")
            note = take_command()
            with open("notes.txt", "a") as f:
                f.write(note + "\n")
            speak("I have saved your note.")

        elif "read notes" in query:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r") as f:
                    notes = f.readlines()
                if notes:
                    speak("Here are your saved notes.")
                    for n in notes:
                        print(f"- {n.strip()}")
                        speak(n.strip())
                else:
                    speak("Your notes file is empty.")
            else:
                speak("No notes found yet.")

        elif "voice" in query:  #  Voice Change
            if "male" in query:
                engine.setProperty("voice", voices[0].id)
                speak("I will now speak in a male voice.")
            elif "female" in query:
                engine.setProperty("voice", voices[1].id)
                speak("I will now speak in a female voice.")

        elif "help" in query:
            show_help()

        elif "exit" in query or "quit" in query:
            speak(f"Goodbye! {APP_NAME} is shutting down. Have a nice day.")
            sys.exit()

        else:        #  Offline Fallback
            # If internet is down, at least say something
            try:
                speak("I can search that for you")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            except:
                speak("Sorry, I am offline. I can only do basic tasks like time, notes, and system commands.")

if __name__ == "__main__":
    print(f" Starting {APP_NAME} AI Assistant ")
    run_ai()
