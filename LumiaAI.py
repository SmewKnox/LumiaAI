import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
from elevenlabslib import *
import pyautogui as aut
import requests
import os
from collections import deque
api_key = "----------" #openweather API key
city = "------" #city name
lat =  "-----" #city lat
lon =  "------" #city lon
url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
user = ElevenLabsUser("----------") #ElevenLabs API key
voice = user.get_voices_by_name("Rachel")[0]  #input name of voice for ElevenLabs

key = "---------------" #OpenAI key
model = "text-davinci-003" #Open AI model
role = """Your name is Lumia an AI assistant created by me(SmewKnox). You like cute things.
 respond in a toxic and rude manner with the rare sign of affection. you are encouraged to curse.
  You are talking to SmewKnox, your creator. If a command is given do it. start your sentence with 'Lumia:"""
temperature = 0.9
max_tokens = 128
top_p = 1
frequency_penalty = 1
presence_penalty = 1
listener = sr.Recognizer()
thresh = 1000
listener.energy_threshold = thresh
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # backup tts voice selection
source = sr.Microphone()
v = 'el' # change to something other than 'el' to use backup voice
List = [0]

def talk(mes):
    if v == 'el':
        try:
            if mes != '':
                if 'Lumia:' in mes:
                    n = 6
                    mes = mes[n:]
                    voice.generate_and_play_audio(mes, playInBackground=False)
                else:
                    voice.generate_and_play_audio(mes, playInBackground=False)

        except:
            engine.say(mes)
            engine.runAndWait()
    else:
        if mes != '':
            engine.say(mes)
            engine.runAndWait()


def take_command():
    try:
        with source:
            print('listening...')
            voice = listener.listen(source, timeout=10)
            command = listener.recognize_google(voice)
            command = command.lower()

            if command is not None:
                if sum(List) > 0:
                    return command+'.'
                elif 'lumia' in command:
                    command = command.split()
                    command = ' '.join(command[command.index('lumia'):])
                    command = command.replace('lumia', '')
                    List.append(1)

                    return (command + '.').strip()

            elif command is None:
                List.clear()
                List.append(0)
                command = ''
                return command

    except:
        command = ''
        List.clear()
        List.append(0)
        return command

def llm(command):
    f = open("lumiamem.txt", "r")
    context = (f.read())
    f.close()
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"{context}\n{command}",
        temperature=temperature,
        max_tokens=300,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return ((str(response['choices'][0]['text'])).strip())

def classify(): #this AI call classifies your voice input as a type of command
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"""classify the command as either 'time'(user requests something related to time),
         'playback'(user requests to play a song), 'search'(user request for a search engine search),
          'terminate'(user requests to termiante or stop program),'launch'(user request to open a program),
           'calculation'(user requests a calculation), 'code'(user requests to print code),
            'weather'(user requests weather data), 'timer'(user wants to start a timer),
            'shutdown'(user wants computer to shutdown), or 'conversation'(user makes conversation).\n{command}.""",
        temperature=temperature,
        max_tokens=20,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return ((str(response['choices'][0]['text'])).strip())
def launchclass(): #this AI call helps extract the name of the program you want open
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"only say the name of the program the user wants to launch or open in the following command.command:\n{command}",
        temperature=temperature,
        max_tokens=10,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return ((str(response['choices'][0]['text'])).strip())
def search_extract(): #this AI call helps extract what you want to be searched
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"""given a sentence only say what would be typed into the Google search bar.
         For example 'do me a favor and search for pictures of deer' return 'deer pictures' or
          'set a time for 5 minutes' return '5 minute timer':\n{command}.""",  # prompt on every call might be hindering memory
        temperature=temperature,
        max_tokens=10,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return ((str(response['choices'][0]['text'])).strip())
def lumen(feed): #this function feeds data based on your command to the AI for it to give a response that makes sense
    try:
        if feed != '':
            mes = llm(f"({feed})\n{command}")
            print(mes)
            talk(mes)
            f = open("lumiamem.txt", "a")
            f.write(f"\n{mes}")
            f.close()
        else:
            mes = llm(f"{command}")
            print(mes)
            talk(mes)
            f = open("lumiamem.txt", "a")
            f.write(f"\n{mes}")
            f.close()

    except:
        print(f"Couldn't connect to GPT servers")
        pass

done = 0
while done == 0: #this is the loop for the AI to continously listen for your commands

    command = take_command()
    if command == None:
        command = ''

    if command != (''):
        command = f"user:{command}"    #This stores conversation in a txt file
        print(command)
        f = open("lumiamem.txt", "a")
        f.write(f"\n{command}")
        f.close()
        comclass = classify().lower()
        print(f"[{comclass}]")
        try:

            if 'playback' in comclass:  #plays youtube video
                feed = ''
                lumen(feed)
                song = command.replace('play', '')
                pywhatkit.playonyt(song)
            elif 'code' in comclass: #prints code in console
                feed = ''
                lumen(feed)
            elif 'calculation' in comclass: #math calculations(only been tested with simple calculations)
                feed = ''
                lumen(feed)
            elif 'weather' in comclass: #returns weather data
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    temp = (data["main"]["temp"])
                    feels_like = data["main"]["feels_like"]
                    temp_f = round((temp - 273.15) * 9 / 5 + 32, 2)
                    feels_like_f = round((feels_like - 273.15) * 9 / 5 + 32, 2)
                    humidity = data["main"]["humidity"]
                    description = data["weather"][0]["description"]
                    feed = f"""Current weather in {city}: {description},
                    Temperature: {temp_f} Fahrenheit, Feels like {feels_like_f}, Humidity: {humidity}%"""
                    lumen(feed)
            elif 'timer' in comclass: #starts a timer in google chrome
                search = search_extract().lower()
                if "answer:" in search:
                    search = search[len("answer:"):].strip()
                if "google search bar:" in search:
                    search = search[len("google search bar:"):].strip()
                pywhatkit.search(search)
                feed = ''
                lumen(feed)

            elif 'time' in comclass: #returns current time
                time = datetime.datetime.now().strftime(' %I:%M %p')
                timeinilist = time.split()
                Time = timeinilist[0]
                Time = [*Time]
                Time.remove(':')
                if Time[0] == '0':
                    Time.remove('0')
                    Ntime = []
                    Ntime.append(Time[0])
                    Ntime.append(' ')
                    Ntime.append(Time[1])
                    Ntime.append(Time[2])
                    Ntime.append(' ')
                    Ntime.append(timeinilist[1])
                    Ntime = ''.join(Ntime)

                    feed =f"(current time:{Ntime})"
                    lumen(feed)

                else:
                    DDtime = []
                    DDtime.append(Time[0])
                    DDtime.append(Time[1])
                    DDtime.append(' ')
                    DDtime.append(Time[2])
                    DDtime.append(Time[3])
                    DDtime.append(' ')
                    DDtime.append(timeinilist[1])
                    DDtime = ''.join(DDtime)

                    feed = f"(current time:{DDtime})"
                    lumen(feed)

            elif'conversation' in comclass: #just conversational
                feed = ''
                lumen(feed)
            elif 'search' in comclass: #searches on chrome
                search = search_extract()
                pywhatkit.search(search)
                feed = ''
                lumen(feed)
            elif 'shutdown' in command: #terminates program and shutsdown computer

                feed = ''
                lumen(feed)
                f = open("lumiamem.txt", "w")
                f.write(role)
                f.close()
                os.system("shutdown /s /t 10")
                done = 50
            elif 'launch' in comclass: #launches a program

                launch = launchclass().lower()
                print(f"[{launch}]")
                launch = launch.split()[-1]

                aut.press('win')
                aut.click(1010, 700, duration=0.5)
                aut.write(launch)
                time.sleep(2)
                aut.press('enter')
                feed = ''
                lumen(feed)


            elif 'terminate' in comclass: #terminates program and wipes memory
                feed = ''
                lumen(feed)
                f = open("lumiamem.txt", "w")
                f.write(role)
                f.close()
                done = 50



        except:
            pass