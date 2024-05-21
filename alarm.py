import pyttsx3
import os
import datetime

engine = pyttsx3.init()
engine.setProperty('volume', 8.0)
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# convert text into speech
def speak(text):
    engine.say(text)

    engine.runAndWait()

extractedtime=open("Alarm.txt","rt")
time = extractedtime.read()
Time= str(time)

extractedtime.close()

deletetime= open("Alarm.txt","r+")
deletetime.truncate(0)
deletetime.close()

def ring(time):
    timeset = str(time)
    timenow = timeset.replace("Jarvis","")
    timenow = timenow.replace("set an alarm","")
    timenow = timenow.replace(" and ",":")

    AlarmTime=str(time)
    print(AlarmTime)
    while True:
        currenttime = datetime.datetime.now().strftime("%H:%M:%S")
        if currenttime ==AlarmTime:
            speak("Alarm ringing, sir")
            os.startfile("LOCATION OF THE SONG")
        elif currenttime+"00:00:30"==AlarmTime:
            exit()

ring(time)
