import pyttsx3
import speech_recognition as sr
import datetime
import os
import requests
import webbrowser
import pywhatkit
import wikipedia
import ecapture
from ecapture import ecapture as ec
import wolframalpha
import pyjokes


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")

    else:
        speak("Good Evening Sir !")

    assname = "Base Voice Assistant"
    speak("I am your Assistant")
    speak(assname)
    speak("How can i Help you, Sir")


def username():
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("How can i help you, sir")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query

if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    username()

    while True:
        query = takeCommand().lower()

        if 'introduce yourself' in query:
            wishMe()

        elif "where is" in query:
            try:
                query = query.replace("where is ", "")
                location = query.lower()
                webbrowser.open("https://www.google.com/maps/place/"+location)
            except:
                speak('An error occurred, please try again')

        elif 'open' in query and len(query.split())==2:
            try:
                query=query.replace("open ", "").lower()
                speak(f"Opening {query}\n")
                webbrowser.open(f"{query}.com")
            except:
                speak('An error occurred, please try again')

        elif 'open google' in query:
            speak("Opening google")
            webbrowser.open("google.com")

        elif 'open youtube' in query:
            speak("Opening youtube")
            webbrowser.open("youtube.com")

        elif 'open stackoverflow' in query:
            speak("Opening stackoverflow")
            webbrowser.open("stackoverflow.com")

        elif 'open github' in query:
            speak("Opening github")
            webbrowser.open("github.com")

        elif 'weather' in query:

            api_key = "YOUR API KEY"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            print("City name : ")
            speak("City name")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature = " +
                      str(int(round(current_temperature - 273.15, 0))) + "°C" + "\n humidity (in percentage) = " + str(
                    current_humidiy) + "%" + "\n description = " + str(weather_description))
                speak('It is'+str(int(round(current_temperature - 273.15, 0))) + "°Celcius" + " with " + str(current_humidiy) + "% humidity and is" + str(weather_description))

            else:
                speak(" City Not Found ")

        elif 'search on wikipedia ' in query:
            speak('Searching Wikipedia...')
            query = query.replace("search on wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'google ' in query:
            query = query.replace("google", '')
            try:
                googleresults = pywhatkit.info(query, lines=3)
                speak('Here is what google says')
                speak(wikipedia.summary(query, sentences=3))
                print(googleresults)
            except:
                speak('I didnt get that')

        elif 'exit' in query:
            speak("Shutting down! Thank you for your time")
            exit()

        elif "camera" in query or "take a photo" in query or 'take a picture' in query:
            ec.capture(0, "Voice Assistant Camera", "voiceassistantimg.jpg")


        elif 'play on youtube' in query.lower():
            try:
                query = query.replace('play on youtube', '')
                speak('Playing on youtube')
                pywhatkit.playonyt(query)
            except:
                speak("An unexpected error occured, please try again")

        elif "write a note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('alexa.txt', 'a')
            strTime =[int(datetime.datetime.now().hour),":",int(datetime.datetime.now().minute),"-",int(datetime.datetime.now().day),'/',int(datetime.datetime.now().month),'/',int(datetime.datetime.now().year),':']
            for i in strTime:
                file.write(str(i))
                file.write(' ')
            file.close()
            file = open('alexa.txt', 'a')
            file.write(str(note))
            file.write('\n')
            speak('Noted it down')
            file.close()

        elif "show note" in query or 'short note' in query:
            speak("Showing Notes")
            file = open("alexa.txt", "r")
            print(file.read())

        elif 'delete all notes' in query:
            file = open('alexa.txt', 'w')
            file.write('')
            speak('Deleted all notes')
            file.close()

        elif "calculate" in query:
            try:
                if 'calculate 9 + 10' in query:
                    speak("The answer is... 21")
                    print("The answer is... 21")
                app_id = "H9ETGV-J7TRTT8YQP"
                client = wolframalpha.Client(app_id)
                indx = query.lower().split().index('calculate')
                query = query.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                print("The answer is " + answer)
                speak("The answer is " + answer)
            except:
                speak('i wasnt able to do that')

        elif 'tell me a joke' in query:
            #speak(pyjokes.get_joke())
            speak('you')
