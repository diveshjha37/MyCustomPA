# Friendly Computer Assistant

A simple Python-based command-line tool that greets the logged-in user and provides system health information using text-to-speech. The tool checks CPU and memory usage, lists top consuming processes, and provides options for checking email, holidays, or system health.

## Features

- **Greeting the user**: The program greets the logged-in user with a friendly message.
- **Check Health**: It displays the CPU and memory usage of your system and checks its overall health (good or bad).
- **Top Processes**: It lists the top 5 CPU-consuming and memory-consuming processes.
- **Interactive Menu**: After showing system health, the program asks the user to choose from several options like checking health, checking email, checking holidays, or exiting.
- **Text-to-Speech**: The program uses the `pyttsx3` library to provide text-to-speech functionality for an interactive, hands-free experience.

## Requirements

Before running the script, you need to install the following Python libraries:

1. `psutil` - To gather system information like CPU and memory usage.
2. `pyttsx3` - To provide text-to-speech functionality.
3. `os` - To fetch the currently logged-in user.

Install the required libraries using `pip`:

```bash
pip install psutil pyttsx3

