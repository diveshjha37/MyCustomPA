import time
import psutil
import pyttsx3
import speech_recognition as sr

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listen for a voice command and return the recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)  # Listen for user input

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()  # Use Google's Speech-to-Text API
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that. Please try again.")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please try again later.")
        return None

def get_system_health():
    """Check the system health based on CPU and memory utilization."""
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    memory_info = psutil.virtual_memory()  # Get memory usage info
    memory_usage = memory_info.percent  # Memory usage percentage

    # Check overall health
    health_status = "Good"
    if cpu_usage > 50 or memory_usage > 70:
        health_status = "Not so good"
    
    return cpu_usage, memory_usage, health_status

def get_top_processes(cpu_usage, memory_usage):
    """Get the top processes based on CPU and memory utilization."""
    cpu_processes = []
    memory_processes = {}
    
    # Iterate over processes and collect data
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            proc.cpu_percent = proc.cpu_percent()  # Get accurate CPU usage for process
            proc_memory = proc.memory_info().rss / 1024 / 1024  # Memory in MB
            
            # Add to the cpu_processes list
            if proc.cpu_percent is not None:
                cpu_processes.append(proc)
            
            # Group processes by name for memory calculation
            if proc.info['name'] not in memory_processes:
                memory_processes[proc.info['name']] = 0
            memory_processes[proc.info['name']] += proc_memory  # Add memory usage for same process name

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle processes that might disappear or cannot be accessed
            continue

    # Sort processes by CPU usage (top 5)
    cpu_processes = sorted(cpu_processes, key=lambda p: p.cpu_percent, reverse=True)[:5]

    # Sort processes by total memory usage (top 5)
    memory_processes_sorted = sorted(memory_processes.items(), key=lambda p: p[1], reverse=True)[:5]

    cpu_top = "\nTop CPU consuming processes:"
    memory_top = "\nTop Memory consuming processes:"

    # Print CPU processes
    for proc in cpu_processes:
        cpu_top += f"\nPID: {proc.info['pid']} - {proc.info['name']} - CPU: {proc.cpu_percent}%"
    
    # Print Memory processes (show total memory in MB for each)
    for name, total_memory in memory_processes_sorted:
        memory_top += f"\n{name} - Memory: {total_memory:.2f} MB"
    
    # Get the top process names for CPU and Memory
    top_cpu_name = cpu_processes[0].info['name'] if cpu_processes else "None"
    top_memory_name = memory_processes_sorted[0][0] if memory_processes_sorted else "None"
    top_memory_value = memory_processes_sorted[0][1] if memory_processes_sorted else 0

    # Convert top memory value from MB to GB for better readability
    top_memory_value_gb = top_memory_value / 1024 if top_memory_value else 0

    return cpu_top, memory_top, top_cpu_name, top_memory_name, top_memory_value, top_memory_value_gb

def handle_health_command():
    """Handle the 'health' command."""
    cpu_usage, memory_usage, health_status = get_system_health()

    # Provide a response based on health status
    if health_status == "Good":
        print(f"Computer: I am in good health. My CPU usage is {cpu_usage}% and memory usage is {memory_usage}%.")
        speak(f"I am in good health. My CPU usage is {cpu_usage}% and memory usage is {memory_usage}%.")
    else:
        print(f"Computer: Currently, my health is not so good. My CPU usage is {cpu_usage}% and memory usage is {memory_usage}%.")
        speak(f"Currently, my health is not so good. My CPU usage is {cpu_usage}% and memory usage is {memory_usage}%.")
                
        # Get and speak about top processes
        cpu_top, memory_top, top_cpu_name, top_memory_name, top_memory_value, top_memory_value_gb = get_top_processes(cpu_usage, memory_usage)
                
        # First print the top CPU and memory processes
        print(cpu_top)
        print(memory_top)
                
        # Now speak the top CPU and memory process names
        print(f"The process with the highest CPU usage is {top_cpu_name}.")
        speak(f"The process with the highest CPU usage is {top_cpu_name}.")
                
        print(f"The process with the highest memory usage is {top_memory_name}, consuming {top_memory_value:.2f} MB ({top_memory_value_gb:.2f} GB).")
        speak(f"The process with the highest memory usage is {top_memory_name}, consuming {top_memory_value:.2f} MB ({top_memory_value_gb:.2f} GB).")

def handle_basic_questions(command):
    """Handle basic questions like 'How are you?', 'What is your name?' etc."""
    if "how are you" in command:
        speak("I'm doing great! Thanks for asking. How are you?")
    elif "what is your name" in command:
        speak("I am your friendly computer assistant. You can call me Assistant!")
    elif "who made you" in command:
        speak("I was created by some really smart engineers at OpenAI. They made me so I can talk to you!")
    elif "what is love" in command:
        speak("Love is a beautiful feeling. It's when you care about someone deeply and want to make them happy.")
    elif "who are you" in command:
        speak("I am your assistant, here to help you with anything you need!")
    else:
        speak("Sorry, I don't understand that question. You can ask me about my health, or ask me my name!")

def main():
    """Main function to listen and respond to commands."""
    print("Hello, Dj! I am your friendly computer. Say 'health' to check system health or ask me some basic questions!")
    speak("Hello, Dj! I am your friend. Say 'health' to check system health or ask me some basic questions!")

    while True:
        command = listen_for_command()

        if command:
            if "health" in command:
                handle_health_command()
            elif "exit" in command:
                print("Computer: Goodbye, human! I will be here waiting to do your bidding. 😎")
                speak("Goodbye, human! I will be here waiting to do your bidding. 😎")
                break
            else:
                handle_basic_questions(command)

if __name__ == "__main__":
    main()
