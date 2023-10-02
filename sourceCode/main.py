# import the necessary modules
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import playsound as ps
import pytz

# create a class called MyGUI
class MyGUI:
    
    # define the init method that creates the GUI
    def __init__(self):
        

        # initialize the tkinter window object
        window = tk.Tk()

        username = input("Please enter your computer's username: ")

        # set the title of the window
        window.title("Phoenix Assistant")
        
        # set the size of the window
        window.geometry("500x420")
        window.resizable(False, False)
        window.attributes("-fullscreen", False)
        
        # set the background color of the window
        window.configure(bg="#f2f2f2")
        
        # set the icon for the window
        window.iconbitmap("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\imageFiles\\icon.ico")

        # create a label for the title
        title_label = tk.Label(window, text="Phoenix Assistant", font=("Calibri", 24, "bold"), bg="#f2f2f2")
        title_label.pack(pady=10)

        # create a label for the commands
        cmd_label = tk.Label(window, text="Password:", font=("Calibri", 14), bg="#f2f2f2")
        cmd_label.pack()

        # create an entry box for the user to input commands
        self.text_box = tk.Entry(window, font=("Calibri", 14))
        self.text_box.pack(pady=10)

        # create a button to allow the user to submit the command
        speak_button = tk.Button(window, text="Submit", background="#008CBA", foreground="white", font=("Calibri", 14), command=self.on_click)
        speak_button.pack(pady=10)

        # create a text box to display output from the assistant
        self.output_text = tk.Text(window, font=("Calibri", 12), height=10, state="disabled")
        self.output_text.pack(pady=10)

        # start the tkinter event loop
        window.mainloop()

    # define the on_click method that is called when the user clicks the submit button
    def on_click(self):
        # get the user's command from the entry box
        input_text = self.text_box.get()
        
        # if the command is "phoenix", call the takeCommand method
        if input_text.lower() == "phoenix":
            self.takeCommand(self.output_text)

    # define the takeCommand method that controls the digital assistant's responses
    def takeCommand(self, output_text):

        # Get the local timezone
        local_tz = pytz.timezone('America/New_York')

        # Set the timezone of the current time to the local timezone
        curr_time = datetime.datetime.now(tz=local_tz)

        # initialize the text-to-speech and speech recognition engines
        engine = pyttsx3.init("sapi5")
        r = sr.Recognizer()
        
        # define a wake-up phrase
        wake_up_phrase = "phoenix"

        # define a method to set the voice settings of the text-to-speech engine
        def set_voice(rate=185, voice_idx=3):
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[voice_idx].id)
            engine.setProperty("rate", rate)

        import threading

        # define a method to allow the assistant to speak
        def speak(audio):
            def _speak():
                engine.say(audio)
                engine.runAndWait()

            threading.Thread(target=_speak).start()


        # set the voice settings and play a starting sound effect
        set_voice()
        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\Start.mp3")

        # set listening to True to start listening for the wake-up phrase
        listening = True

        # start the loop to listen for user commands
        while True:
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source, timeout=5) # wait for command for 5 seconds
            try:
                # transcribe the user's speech to text
                query = r.recognize_google(audio, language="en-in")

                # check if the wake-up phrase was spoken
                if listening and wake_up_phrase in query:
                    # turn off listening to allow for response
                    listening = False

                    # say a response and wait for it to finish
                    speak("How can I help you?")
                    engine.runAndWait()

                    # continue listening for new commands
                    listening = True
                    continue

                # if not listening, continue to the next iteration of the loop
                if listening:
                    output_text.configure(state="normal")
                    output_text.insert(tk.END, f"Command: {query}\n")
                    output_text.configure(state="disabled")

                    # check for various commands and respond accordingly
                    if "wikipedia" in query:
                        ps.playsound("End.mp3")
                        speak("Searching Wikipedia...")
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=2)
                        speak("According to Wikipedia")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, f"According to Wikipedia:\n{results}\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")
                    elif "on YouTube" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening Youtube...")
                        query = query.replace(" on youtube", "")
                        webbrowser.open(f"youtube.com/results?search_query={query}")

                    elif "on Google" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening Google...")
                        query = query.replace("on Google", "")
                        webbrowser.open(f"google.com/search?q={query}")

                    elif "open stackoverflow" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening StackOverflow...")
                        webbrowser.open("stackoverflow.com")

                    elif "time" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")

                        # Get the current time in the local timezone
                        curr_time = datetime.datetime.now(tz=local_tz)

                        strTime = curr_time.strftime("%I:%M %p")
                        speak(f"The current time is {strTime}")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, f"The current time is {strTime}\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    elif "date" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")

                        # Get the current time in the local timezone
                        curr_time = datetime.datetime.now(tz=local_tz)

                        strTime = curr_time.strftime("%d/%m/%Y")
                        speak(f"The current date is {strTime}")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, f"The current date is {strTime}\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    elif "file" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening File Explorer...")
                        output_text.insert(tk.END, "Opening File Explorer...\n")
                        output_text.insert(tk.END, " \n")
                        os.startfile("C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\File Explorer")

                    elif "open Notepad" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening Notepad...")
                        output_text.insert(tk.END, "Opening Notepad...\n")
                        output_text.insert(tk.END, " \n")
                        os.startfile("C:\\Windows\\system32\\notepad.exe")

                    elif "open command prompt" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("Opening Command Prompt...")
                        output_text.insert(tk.END, "Opening Command Prompt...\n")
                        output_text.insert(tk.END, " \n")
                        os.startfile("C:\\Windows\\system32\\cmd.exe")

                    elif "help" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        speak("For a list of commands, please view the command list shown in the console.")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, " \n")
                        output_text.insert(tk.END, "--------------------------- Command List ----------------------------\n")
                        output_text.insert(tk.END, "- Wikipedia search: <query> ---- Searches wikipedia for '<query>'\n")
                        output_text.insert(tk.END, "- Open Youtube: <query> on youtube ---- Searches youtube for '<query>'\n")
                        output_text.insert(tk.END, "- Open Google: <query> on google ---- Searches google for '<query>'\n")
                        output_text.insert(tk.END, "- Hello ---- Says hello\n")
                        output_text.insert(tk.END, "- Open StackOverflow ---- Opens StackOverflow\n")
                        output_text.insert(tk.END, "- Play music ---- Not yet implemented\n")
                        output_text.insert(tk.END, "- Time ---- Displays the current time\n")
                        output_text.insert(tk.END, "- Date ---- Displays the current date\n")
                        output_text.insert(tk.END, "- Open File ---- Opens File Explorer\n")
                        output_text.insert(tk.END, "- Open Notepad ---- Opens Notepad\n")
                        output_text.insert(tk.END, "- Open Command Prompt ---- Opens Command Prompt\n")
                        output_text.insert(tk.END, "- Open Code ---- Opens Visual Studio Code\n")
                        output_text.insert(tk.END, "- What's your name? ---- Gives the name 'Phoenix'\n")
                        output_text.insert(tk.END, "- How old are you? ---- Tells the age of 'Phoenix'\n")
                        output_text.insert(tk.END, "- Who made you? ---- Tells who made 'Phoenix'\n")
                        output_text.insert(tk.END, "-------------------------- Command List ----------------------------\n")
                        output_text.insert(tk.END, " \n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")


                    elif "open code" in query:
                        ps.playsound("C:\\Program Files (x86)\\Phoenix\\phoenixResources\\soundFiles\\End.mp3")
                        codePath = "C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                        os.startfile(codePath)
                        speak("Opening Visual Studio Code...")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, "Opening Visual Studio Code...\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    elif "thank you" in query:
                        speak("You are welcome!")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, "You are welcome!\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    elif "your name" in query:
                        speak("My name is Phoenix!")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, "My name is Phoenix!\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    elif "how old are you" in query:
                        speak("My birthday is September 4th, 2023. I have much to learn!")
                        output_text.insert(tk.END, "My birthday is September 4th, 2023. I have much to learn!")
                        output_text.insert(tk.END, " \n")

                    elif "who made you" in query:
                        speak("I was created by Allen Anderson.")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, "I was created by Allen Anderson.\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

                    else:
                        speak("Sorry, I don't understand. Please try again.")
                        output_text.configure(state="normal")
                        output_text.insert(tk.END, "Sorry, I don't understand. Please try again.\n")
                        output_text.insert(tk.END, " \n")
                        output_text.configure(state="disabled")

            except sr.WaitTimeoutError:
                # move on to the next iteration of the loop if no command is detected in 5 seconds
                continue
                    
            except Exception as e:
                speak("Something went wrong. Please try again.")
                output_text.configure(state="normal")
                output_text.insert(tk.END, "Something went wrong. Please try again.\n")
                output_text.insert(tk.END, " \n")
                output_text.configure(state="disabled")
        
            # break out of the loop and return control to the GUI
            # after a command has been detected and responded to
            break

# define a method to run the MyGUI class
def run_GUI(MyGUI):
    
    return MyGUI()

# create an instance of MyGUI
gui = run_GUI(MyGUI)