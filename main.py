import ollama
import speech_recognition as sr
import pyttsx3
import datetime
import os
import subprocess
import requests

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Select the first available voice

    def speak(self, text):
        print(f"Assistant: {text}")  # Debug log
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=5)
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Prevent infinite waiting
                said = recognizer.recognize_google(audio)
                print(f"User: {said}")  # Debug log
                return said.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                self.speak("I could not understand that. Please say it again.")
            except sr.RequestError as e:
                print(f"Request error: {e}")
                self.speak("There is a problem with the speech recognition service.")
            except Exception as e:
                print(f"Exception: {str(e)}")
                self.speak("An error occurred. Please try again.")
        return ""

class OllamaService:
    def __init__(self):
        pass

    def get_response(self, prompt):
        try:
            response = ollama.chat(model='mistral', messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Ollama Service Error: {e}")
            return "Sorry, I couldn't process your request due to an error."

class Tasks:
    def __init__(self, assistant, ollama_service):
        self.assistant = assistant
        self.ollama_service = ollama_service

    def tell_date_time(self, command):
        now = datetime.datetime.now()
        date = now.strftime("%B %d, %Y")
        time = now.strftime("%I:%M %p")
        
        if "date" in command and "time" in command:
            self.assistant.speak(f"Today's date is {date} and the current time is {time}")
        elif "date" in command:
            self.assistant.speak(f"Today's date is {date}")
        elif "time" in command:
            self.assistant.speak(f"The current time is {time}")

    def calculate_sum(self, command):
        numbers = [int(word) for word in command.split() if word.isdigit()]
        if len(numbers) == 2:
            result = sum(numbers)
            self.assistant.speak(f"The sum of {numbers[0]} and {numbers[1]} is {result}")
        else:
            self.assistant.speak("Please provide two numbers to calculate the sum.")
    
    def open_application(self, command):
        applications = {
            "notepad": "notepad.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "paint": "mspaint.exe",
            "browser": "chrome.exe",
            "cmd": "cmd.exe"
        }
        for app_name, process_name in applications.items():
            if app_name in command:
                subprocess.Popen(process_name, shell=True)
                self.assistant.speak(f"Opening {app_name}")
                return
        self.assistant.speak("Application not recognized. Please try again.")
    
    def close_application(self, command):
        applications = {
            "notepad": "notepad.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "paint": "mspaint.exe",
            "browser": "chrome.exe",
            "cmd": "cmd.exe"
        }
        for app_name, process_name in applications.items():
            if app_name in command:
                result = subprocess.run(f'taskkill /f /im {process_name}', shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.assistant.speak(f"{app_name} closed successfully.")
                else:
                    self.assistant.speak(f"{app_name} is not open.")
                return
        self.assistant.speak("Application not recognized. Please try again.")
    
    def ollama_interaction(self, command):
        response = self.ollama_service.get_response(command)
        self.assistant.speak(response)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    ollama_service = OllamaService()
    tasks = Tasks(assistant, ollama_service)
    
    assistant.speak("Hello Sir, how can I help you?")
    while True:
        command = assistant.listen()
        if command:
            if "date" in command or "time" in command:
                tasks.tell_date_time(command)
            elif "sum" in command:
                tasks.calculate_sum(command)
            elif "open" in command:
                tasks.open_application(command)
            elif "close" in command:
                tasks.close_application(command)
            elif "use lama" in command:
                command = command.replace("use lama", "").strip()
                tasks.ollama_interaction(command)
            elif "exit" in command or "quit" in command or "goodbye" in command:
                assistant.speak("Goodbye Sir!")
                break
            else:
                assistant.speak("I didn't understand that. Please try again.")
        else:
            print("No command recognized.")
