import time
import psutil
import pyttsx3

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

def speak(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def get_system_health():
    """Check the system health based on CPU and memory utilization."""
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    memory_info = psutil.virtual_memory()  # Get memory usage info
    memory_usage = memory_info.percent  # Memory usage percentage

    # Check overall health
    health_status = "Good"
    if cpu_usage > 50 or memory_usage > 50:
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

def menu():
    """Display a menu of options to the user."""
    speak("Please choose an option:")
    print("1. Check Health")
    print("2. Check Email")
    print("3. Check Holidays")
    print("4. Exit")
    speak("1. Check Health. 2. Check Email. 3. Check Holidays. 4. Exit.")
    
    user_input = input("You: ")
    if user_input == '1' or 'check health' in user_input.lower():
        print("You selected: Check Health")
        speak("You selected Check Health.")
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

        # Ask the user for the next option
        menu()
    
    elif user_input == '2' or 'check email' in user_input.lower():
        print("You selected: Check Email")
        speak("You selected Check Email.")
        # Placeholder for email checking logic (can be added later)
        speak("Email checking functionality is under construction.")
    
    elif user_input == '3' or 'check holidays' in user_input.lower():
        print("You selected: Check Holidays")
        speak("You selected Check Holidays.")
        # Placeholder for holiday checking logic (can be added later)
        speak("Holiday checking functionality is under construction.")
    
    elif user_input == '4' or 'exit' in user_input.lower():
        print("Computer: Goodbye, human! I will be here waiting to do your bidding. 😎")
        speak("Goodbye, human! I will be here waiting to do your bidding. 😎")
    else:
        print("Computer: Invalid choice. Please select a valid option.")
        speak("Invalid choice. Please select a valid option.")
        menu()

def talk_to_computer():
    print("Hello, human! I am your friendly computer. What do you want to talk about?")
    speak("Hello, human! I am your friendly computer. What do you want to talk about?")
    time.sleep(2)
    
    # Start the menu
    menu()

talk_to_computer()
