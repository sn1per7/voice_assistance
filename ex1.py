import speech_recognition as sr
import os
from weather import Weather
import webbrowser
import smtplib
import re
from gtts import gTTS
import requests
import pyttsx3
import sys
import googlesearch
import google


def ask():
    # function to listen command (speech recognition)
    r = sr.Recognizer()

    with sr.Microphone() as source:
        speak("I am listening")
        r.pause_threshold = 1
        r.energy_threshold = 1000
        r.dynamic_energy_threshold = True
        r.dynamic_energy_adjustment_damping = 0.15
        r.dynamic_energy_ratio = 1.5
        r.operation_timeout = None
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=0.5, phrase_time_limit=5)

    try:
        command = r.recognize_google(audio).lower()
        print("You said :" + command + "\n")

    except sr.UnknownValueError:
        speak("Your last command is not audible!!! Please repeat...")
        command = ask()

    return command


def speak(audio):
    # function to speak action (text to speech)

    # #print(audio)
    # text_to_speech = gTTS(text="audio", lang='en')
    # text_to_speech.save("audi.mp3")
    # os.system("mpg321 audi.mp3")
    print(audio)
    engine = pyttsx3.init()
    # voices = engine.getProperty("voices")
    # for voice in voices:
    # engine.setProperty("voices", voice.id)
    engine.say(audio)
    engine.runAndWait()


name = "null"


def assistance(command):
    # function to process command
    global name
    if "hello" in command:
        if name=="null":
            speak("hey. my name is sniper. what is your name?")
            print(name)
            name = ask()
            print(name)
            speak("ok i remembered your name as " + name)
        else:
            speak("hey! " + name + " how can i help you ")

    elif "hey" in command:
        if name=="null":
            speak("hello. my name is sniper. what is your name?")
            print(name)
            name = ask()
            print(name)
            speak("ok i remembered your name as " + name)
        else:
            speak("hello! " + name + " how can i help you ")

    elif "what is my name" in command:
        print(name)
        if name == "null":
            speak("sorry, you did not tell your name yet")
        else:
            speak("your name is " + name)

    elif "open website" in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www." + domain
            webbrowser.open(url)
            speak("done...")
        else:
            speak("website not exist")

    elif "search" in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            for j in googlesearch.search(domain, tld="co.in", num=5, stop=1, pause=2):
                webbrowser.open(j)
                print(j)
        else:
            speak("search not available")

    elif "email" in command:
        speak("whom do you want to mail")
        receiver_name = ask()
        print(receiver_name)
        speak("email id ?")
        receiver_email = ask()



        speak("what is the message?")
        msg = ask()
        print(msg)
        mail = smtplib.SMTP("smtp.gmail.com", 587)      #initiate gmail SMPT
        print(msg)
        mail.ehlo()     #indentify the server
        mail.starttls()     #encrypt session
        username = "simransinghoff@gmail.com"
        password = "simranoff"
        mail.login(username, password)

        mail.sendmail(receiver_name,receiver_email , msg)
        speak("email send ")
        mail.close()

    elif " weather in " in command:
        reg_ex = re.search('weather in (.+)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            speak("The current weather in %s is %s The temperature is %.lf degree" % (city, condition.text(), (int(condition.temp())-32)/1.8))


    elif "bye" in command:
        speak("good bye, see you later")
        exit()

# ask()
# audio = "hey sniper! you are brillient"
# speak(audio)

speak("I am ready!!!")

while True:
    assistance(ask())
