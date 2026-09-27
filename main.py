from dotenv import load_dotenv
from openai import OpenAI
# import google.generativeai as genai
import time
import speech_recognition as sr
import webbrowser
import edge_tts
import asyncio
import pygame
import glob
import os
import musicLibrary
import requests

pygame.mixer.init()
for file in glob.glob("voice_*.mp3"):
    try:
        os.remove(file)
    except:
        pass
load_dotenv()
client=OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
newsapi=os.getenv("NEWS_API_KEY")

async def speak_async(text):
    filename = f"voice_{int(time.time()*1000)}.mp3"

    try:
        communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
        await communicate.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            pass

        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

def speak(text):
    asyncio.run(speak_async(text))
def ask_ai(prompt):
    response=client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role":"system","content":"You are a helpful assistant."},
                  {"role":"user","content":prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open twitter" in c.lower():
        speak("Opening Twitter")
        webbrowser.open("https://www.x.com")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif "open github" in c.lower():
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")
    elif "open stackoverflow" in c.lower():
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif "open reddit" in c.lower():
        speak("Opening Reddit")
        webbrowser.open("https://www.reddit.com")
    elif "open quora" in c.lower():
        speak("Opening Quora")
        webbrowser.open("https://www.quora.com")
    elif "open wikipedia" in c.lower():
        speak("Opening Wikipedia")
        webbrowser.open("https://www.wikipedia.org")
    elif "open amazon" in c.lower():
        speak("Opening Amazon")
        webbrowser.open("https://www.amazon.com")
    elif "open flipkart" in c.lower():
        speak("Opening Flipkart")
        webbrowser.open("https://www.flipkart.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        if song in musicLibrary.music:
            speak(f"Now Playing {song}. Enjoy!")
            link=musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have the song {song} in my music library.")
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get("articles", [])
            for article in articles:
                speak("Here is a news headline:")
                speak(article['title'])
    elif "time" in c.lower():
        current_time=time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in c.lower():
        current_date=time.strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "calculate" in c.lower():
        expression=c.lower().replace("calculate", "").strip()
        expression=expression.replace("plus", "+").replace("minus", "-").replace("x", "*").replace("divided by", "/")
        try:
            result=eval(expression)
            print(f"The result of {expression} is {result}")
            speak(f"The result of {expression} is {result}")
        except Exception as e:
            speak(f"Sorry, I couldn't calculate that. Error: {e}")

    else:
        speak("Let me check that for you.")
        response=ask_ai(c) 
        speak(str(response))


if __name__ == "__main__":
  speak("Initializing Jarvis......")
 
  while True:
      # Listen for wake word  "Jarvis"
      r=sr.Recognizer()
      print("Recognizing...")
      try:
        with sr.Microphone() as source:
                 print("Listening..")
                 r.adjust_for_ambient_noise(source, duration=1)
                 audio=r.listen(source, timeout=5, phrase_time_limit=5)
        word=r.recognize_google(audio)
        print(f"You said: {word}")

        if "Jarvis" in word.lower() or "hello" in word.lower(): 
            speak("ya")
            #listen for command
            with sr.Microphone() as source:
               
                r.adjust_for_ambient_noise(source, duration=1)
                audio=r.listen(source, timeout=5, phrase_time_limit=5)
                command=r.recognize_google(audio)
                print(f"Command: {command}")

            processCommand(command)
      except sr.UnknownValueError:
        print("Could not understand audio")
      except sr.RequestError as e:
        print(f"Google Api Error; {e}")
      except Exception as e:
          print(f"Could not request results: {e}")