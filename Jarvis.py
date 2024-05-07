import time
from time import sleep
import pynput.keyboard
import speedtest
import pyttsx3
import speech_recognition as sr
import datetime
import pyaudio
import os
import webbrowser
import pywhatkit as kit
from config import apikey
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import pyautogui
import cv2
import pyjokes
from datetime import timedelta
import keyboard

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 5.0)
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# convert text into speech
def speak(text):
    engine.say(text)

    engine.runAndWait()


# convert our voice to speech
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=5
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")

    except sr.UnknownValueError:
      speak("Can't recognize that")
      return "none"
    return query


# to make jarvis wish you
def wish():
    hour = int(datetime.datetime.now().hour)
    min = int(datetime.datetime.now().minute)
    if (hour >= 6) and (hour < 12):
      speak(f"Good Morning sir it is {hour, min} AM")

    elif (hour >= 12) and (hour < 17):
       speak(f"Good Afternoon sir it is {hour, min} PM ")

    elif (hour >= 17) and (hour < 20):
      speak(f"Good Evening sir it is {hour, min} PM ")

    elif(hour>=20) and (hour<24):
      speak(f"Good Night sir it is {hour, min} PM ")

    elif(hour>=00) and (hour<5):
      speak(f"Good Night sir it is {hour, min} AM")
    speak("Please tell me how can I assist you")


def chat(query):

    global chatstr
    chatstr = ""
    print(chatstr)
    chatstr+=f"User: {query}"
    GOOGLE_API_KEY="YOUR_APIKEY"
    genai.configure(api_key=GOOGLE_API_KEY)


    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat()
    convo.send_message(chatstr)
    print(f"Jarvis: {convo.last.text}")
    speak(f"Jarvis: {convo.last.text}")



def alarm(query):
    timehere=open("Alarm.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def news():

    newsurl="https://newsapi.org/v2/everything?q=Apple&from=2024-04-15&sortBy=popularity&apiKey=96ec2e7739164d0fa1f748784ee162f3"
    main_page = requests.get(newsurl).json()
    articles = main_page["articles"]
    head=[]
    day = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"Today's {day[i]} news is: {head[i]}")

def message():
    speak("Who do you want to message")
    num=int(input(" "))
    hour = int(datetime.datetime.now().strftime("%H"))
    min = int((datetime.datetime.now() + timedelta(minutes=2)).strftime("%M"))
    speak("What's the message sir")
    send_message=str(input(" "))
    kit.sendwhatmsg(f"+91{num}",send_message,hour,min)









if __name__ == '__main__':





    while True:
         query = takecommand()
         if "Hey Jarvis".lower() in query.lower():
            wish()
            while True:
                query=takecommand()

                if "open Whatsapp".lower() in query.lower():
                   path = "C:\\Users\\N C PAUL\\Desktop\\WhatsApp.lnk"
                   speak("Opening WhatsApp sir")
                   os.startfile(path)


                elif "close Whatsapp".lower() in query.lower():
                    speak("Closing Whatsapp sir")
                    os.system("taskkill /f /im WhatsApp.exe")

                elif "open Zoom".lower() in query.lower():
                  npath = "C:\\Users\\N C PAUL\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
                  speak("Opening Zoom sir")
                  os.startfile(npath)

                elif "close zoom".lower() in query.lower():
                    speak("Closing Zoom sir")
                    os.system("taskkill /f /im Zoom.exe")

                elif "show wi-fi speed".lower() in query.lower():
                    wifi = speedtest.Speedtest()
                    upload_speed = wifi.upload()/1048576
                    download_speed = wifi.download()/1048576
                    print("Wi-fi upload speed is",upload_speed)
                    print("Wi-fi download speed is",download_speed)
                    speak(f"Wi-fi upload speed is {upload_speed}")
                    speak(f"Wi-fi download speed is {download_speed}")
                    time.sleep(2)

                elif "send message".lower() in query.lower():
                    message()

                elif "open Google".lower() in query.lower():
                  speak("Sir, what should I search on google")
                  cm=takecommand().lower()
                  speak(f"Searching {cm}")
                  webbrowser.open(cm)

                elif "open YouTube".lower() in query.lower():
                  speak("Sir, what should I search on YouTube")
                  dm=takecommand().lower()
                  speak(f"Searching {dm}")
                  kit.playonyt(dm)

                elif "pause video".lower() in query.lower():
                    pyautogui.press("k")
                    speak("video paused")
                elif "play video".lower() in query.lower():
                    pyautogui.press("k")
                    speak("playing video")
                elif "mute video".lower() in query.lower():
                    pyautogui.press("m")
                    speak("video muted")
                elif "unmute video".lower() in query.lower():
                    pyautogui.press("m")
                    speak("video unmuted")
                elif "open cinema mode".lower() in query.lower():
                    pyautogui.press("t")
                    speak("enabled cinema mode")
                elif "exit cinema mode".lower() in query.lower():
                    pyautogui.press("t")
                    speak("disabled cinema mode")

                elif "full screen".lower() in query.lower():
                    pyautogui.press("f")
                    speak("enabled fullscreen")
                elif "exit full screen".lower() in query.lower():
                    pyautogui.press("f")
                    speak("disabled fullscreen")
                elif "open miniplayer mode".lower() in query.lower():
                    pyautogui.press("i")
                    speak("enabled miniplayer mode")
                elif "expand miniplayer mode".lower() in query.lower():
                    pyautogui.press("i")
                    speak("miniplayer mode expanded")
                elif "open caption".lower() in query.lower():
                    pyautogui.press("c")
                    speak("enabled captions")
                elif "close caption".lower() in query.lower():
                    pyautogui.press("c")
                    speak("disabled captions")
                elif "volume up".lower() in query.lower():
                    from keyboard import volumeup
                    speak("Increasing volume sir")
                    volumeup()
                elif "volume down".lower() in query.lower():
                    from keyboard import volumedown
                    speak("Decreasing volume sir")
                    volumedown()

                elif "open camera".lower() in query.lower():
                    speak("Opening camera sir")
                    cap = cv2.VideoCapture(0)

                    ret, img=cap.read()
                    if ret:
                        cv2.imshow('webcam',img)
                        speak("Sir what should be the name of the image")
                        image=takecommand().lower()
                        speak("Okay sir")
                        speak("Done sir, image is saved on your device")
                        cv2.imwrite(f"{image}.png",img)
                        k=cv2.waitKey(50)
                        if k==27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()

                elif "switch the window".lower() in query.lower():
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")

                elif "tell me the news".lower() in query.lower():
                    speak("Please wait sir, collecting the news")
                    news()

                elif "what is the weather today in".lower() in query.lower():
                    search = "weather in Kasba"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    print(f"Current {search} is {temp}")
                    speak(f"Current {search} is {temp}")

                elif "set an alarm".lower() in query.lower():
                    print("Input format: hr and min and sec")
                    speak("Set the time")
                    a = input("Please tell the time: ")
                    alarm(a)
                    speak("Done, sir")

                elif "remember that".lower() in query.lower():
                    remembermsg = query.replace("remember that","")
                    speak("You told me "+remembermsg)
                    remember = open("Remember.txt","a")
                    remember.write(remembermsg)
                    remember.close()

                elif "what do you remember now".lower() in query.lower():
                    remember = open("Remember.txt","r")
                    speak("You told me"+remember.read())

                elif "play music".lower() in query.lower():
                  music = "D:\\Software Back up\\Entertainment\\Songs\\Music"
                  songs = os.listdir(music)
                  for song in songs:
                    if song.endswith('.mp3'):
                        speak("Playing music sir")
                        os.startfile(os.path.join(music, song))

                elif "I am tired".lower() in query.lower():
                    speak("Playing your favourite songs")
                    webbrowser.open("https://open.spotify.com/playlist/2SNI12ibWSwJ4gJazGPz0X")

                elif "tell me a joke".lower() in query.lower():
                    joke = pyjokes.get_joke()
                    print(f"Jarvis: {joke}")
                    speak(joke)

                elif "take a screenshot".lower() in query.lower():
                    speak("Sir, what should be the name of the screenshot")
                    sc = takecommand().lower()
                    speak("Okay sir, taking a screenshot")
                    time.sleep(5)
                    image = pyautogui.screenshot()


                    image.save(f"{sc}.png")

                elif "shutdown the system".lower() in query.lower():
                    os.system("shutdown /s /t 5")

                elif "restart the system".lower() in query.lower():
                    os.system("shutdown /r /t 5")

                elif "sleep the system".lower() in query.lower():
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


                elif "Jarvis Quit".lower() in query.lower():
                  speak("Ok sir. Quitting. Have a nice day sir.")
                  exit()

                sites = [["spotify","https://open.spotify.com/"],["messenger","https://www.messenger.com/"],
                 ["stack overflow","https://www.stackoverflow.com"],["facebook","https://www.facebook.com"],
                 ["Instagram","https://www.instagram.com"],["Chat","https://www.instagram.com/direct/inbox/"]
                 ,["High Anime","https://hianime.to/home"],["SLS campuscare","https://www.slscampuscare.in/"],
                 ["Gmail","https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"],["Amazon","https://www.amazon.in/"],
                 ["Bing","https://www.bing.com/"],["Wikipedia","https://www.wikipedia.com"],
                  ["Google","https://www.google.com/"],["Web","https://web.whatsapp.com/"]]
                for site in sites:
                  if f"Open {site[0]}".lower() in query.lower():
                    speak(f"Opening {site[0]} sir")
                    webbrowser.open(site[1])
                  elif f"Close {site[0]}".lower() in query.lower():
                      speak(f"Closing {site[0]} sir")
                      pyautogui.hotkey('ctrl', 'w')

                else:

                  chat(query)

