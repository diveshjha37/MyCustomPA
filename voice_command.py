import speech_recognition as sr
import os
import platform

def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("API unavailable.")
            return None

def interpret_command(command):
    if "logout" in command:
        return "logout"
    elif "shutdown" in command:
        return "shutdown"
    elif "restart" in command:
        return "restart"
    elif "open calculator" in command:
        return "open_calculator"
    elif "close calculator" in command:
        return "close_calculator"
    elif "open notepad" in command:
        return "open_notepad"
    elif "close notepad" in command:
        return "close_notepad"
    elif "open browser" in command:
        return "open_browser"
    elif "close browser" in command:
        return "close_browser"
    elif "close all applications" in command:
        return "close_all"
    else:
        return None

def execute_command(action):
    os_name = platform.system()

    if action == "logout":
        if os_name == "Windows":
            os.system("shutdown -l")
        elif os_name in ["Linux", "Darwin"]:
            os.system("pkill -KILL -u $USER")

    elif action == "shutdown":
        if os_name == "Windows":
            os.system("shutdown /s /t 1")
        elif os_name == "Linux":
            os.system("poweroff")
        elif os_name == "Darwin":
            os.system("sudo shutdown -h now")

    elif action == "restart":
        if os_name == "Windows":
            os.system("shutdown /r /t 1")
        elif os_name == "Linux":
            os.system("reboot")
        elif os_name == "Darwin":
            os.system("sudo shutdown -r now")

    elif action == "open_calculator":
        if os_name == "Windows":
            os.system("start calc")
        elif os_name == "Linux":
            os.system("gnome-calculator &")
        elif os_name == "Darwin":
            os.system("open -a Calculator")

    elif action == "close_calculator":
        if os_name == "Windows":
            os.system("taskkill /IM calc.exe /F")
        elif os_name == "Linux":
            os.system("pkill gnome-calculator")
        elif os_name == "Darwin":
            os.system("pkill Calculator")

    elif action == "open_notepad":
        if os_name == "Windows":
            os.system("start notepad")
        elif os_name == "Linux":
            os.system("gedit &")
        elif os_name == "Darwin":
            os.system("open -a TextEdit")

    elif action == "close_notepad":
        if os_name == "Windows":
            os.system("taskkill /IM notepad.exe /F")
        elif os_name == "Linux":
            os.system("pkill gedit")
        elif os_name == "Darwin":
            os.system("pkill TextEdit")

    elif action == "open_browser":
        if os_name == "Windows":
            os.system("start chrome")  # Assumes Chrome is installed
        elif os_name == "Linux":
            os.system("xdg-open https://www.google.com &")
        elif os_name == "Darwin":
            os.system("open -a Safari")

    elif action == "close_browser":
        if os_name == "Windows":
            os.system("taskkill /IM chrome.exe /F")  # Closes Chrome
        elif os_name == "Linux":
            os.system("pkill firefox")  # Change to the browser you use
        elif os_name == "Darwin":
            os.system("pkill Safari")

    elif action == "close_all":
        if os_name == "Windows":
            os.system("taskkill /F /IM *")
        elif os_name == "Linux" or os_name == "Darwin":
            os.system("pkill -9 -u $USER")

    else:
        print("Command not recognized.")

if __name__ == "__main__":
    while True:
        command = listen_to_command()
        if command:
            action = interpret_command(command)
            if action:
                execute_command(action)
            else:
                print("Sorry, I don't know how to do that.")
