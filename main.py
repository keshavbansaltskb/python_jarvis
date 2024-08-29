import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pygame
import os

recognizer  = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "8d46767cb2d74c218b977ddf7bc5a5e3"

def initialize_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Choose the first voice or any other voice in the list
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)  # Adjust speed (words per minute)
    return engine

def speak(text):
    engine = initialize_tts()
    engine.say(text)
    engine.runAndWait()


"""def speak_old(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
"""

def get_wikipedia_summary(query):
    # Replace spaces in query with underscores for Wikipedia URL format
    query = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract paragraphs
        paragraphs = soup.find_all('p')
        summary = []

        # Limit to the first 2 paragraphs for a brief summary
        for i, paragraph in enumerate(paragraphs[:2]):
            summary.append(paragraph.get_text())

        return "\n".join(summary) if summary else "No relevant information found."
    else:
        return "Failed to retrieve information."
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    elif c.lower().startswith("open"):
        webbrowser.open(f"https://{c.lower().split(" ")[1]}.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        song = song.lower()
        link = musicLibrary.music[song]
        webbrowser.open(link)
        

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
        # Parse the JSON response
            data = r.json()

            articles = data.get('articles',[])
            for article in articles[:2]: 
                print(article['title'])
                speak(article['title'])
    
    else:
        phrases_to_remove = ["what is","who is", "who are", "where is", "when is", "how is", "why is", "what are", "who were"]
        query_lower = c.lower()
        for phrase in phrases_to_remove:
            if query_lower.startswith(phrase):
                answer =  c[len(phrase):].strip()

        answer = get_wikipedia_summary(answer)
        print(answer)
        speak(answer)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                audio = r.listen(source,timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes Sir, How may i help you")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))