import google.generativeai as genai
import speech_recognition as sr
import emoji as em
import os
from google.cloud import texttospeech_v1
import time
from datetime import datetime 
import requests
import pywhatkit
import pyautogui
import time
import winsound
import music as spo
import sys

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY= 'your-openweatherapi-key'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path-to-your=api=key'

client = texttospeech_v1.TextToSpeechClient()

genai.configure(api_key='your-api-key')

model = genai.GenerativeModel('gemini-pro')
os.system('cls' if os.name == 'nt' else 'clear')
    
r = sr.Recognizer()

os.system('cls' if os.name == 'nt' else 'clear')

def read_aloud(input_text):
    input_text = texttospeech_v1.SynthesisInput(text=input_text)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16,
        speaking_rate=1.4
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    with open('output.mp3', 'wb') as f:
        f.write(response.audio_content)
    
    winsound.PlaySound("./output.mp3",winsound.SND_FILENAME)
    
def introduction():
    text = 'Hello, I am Nova. Your personal voice assistant.'
    current_time = datetime.now().time()
    if current_time.hour < 12:
        print("Good morning, happy soul." )
        msg="Good morning happy soul"
        read_aloud(msg)
        time.sleep(0.5)
        print(text)
        read_aloud(text)
    elif current_time.hour < 18:
        print("Good afternoon, happy soul")
        msg1="Good afternoon happy soul" 
        read_aloud(msg1)
        time.sleep(0.5)
        print(text)
        read_aloud(text)
    else:
        print("Good evening, happy soul")
        msg2="Good evening happy soul" 
        read_aloud(msg2)
        time.sleep(0.5)
        print(text)
        read_aloud(text)

def generate(prompt):
    response = model.generate_content(["You will generate answers within 75 tokens. Write in a continuous flow, avoiding bulleted lists." + prompt])
    print("Nova:", response.text)
    read_aloud(response.text)

def weather(city):
    text="Here are your results"
    print("Nova :" + str(text))
    read_aloud(text)
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    temp_kelvin=response['main']['temp']
    temp=temp_kelvin - 273.15
    print("Temparature: {:.2f}".format(temp))
    temptext="The temparature is {:.2f}".format(temp) + "Celsius"
    read_aloud(temptext)
    feels_like_kelvin = response['main']['feels_like']
    feels_like=feels_like_kelvin-273.15
    print("Feels like : {:.2f}".format(feels_like))
    feeltext="It feels like it is {:.2f}".format(feels_like) + "Celsius"
    read_aloud(feeltext)
    humidity = response['main']['humidity']
    print("Humidity: ",humidity,"%")
    humidtext="The humidity is" + str(humidity) + "%"
    read_aloud(humidtext)
    wind_speed = response['wind']['speed']
    print("wind speed: ",wind_speed,"m/s")
    windtext="The wind speed is" + str(wind_speed) + "meters per second"
    read_aloud(windtext)
    
def send_msg(msg,person):
    c=datetime.now()
    time=c.strftime('%H:%M:%S')
    hour=int(time[0:2])
    m=int(time[3:5])+1
    sec=int(time[6:8])
    if sec>=50:
        m+=1
    if m>=60:
        m=m%60
        hour+=1
    if hour==24:
        hour=0
    sending(msg,person,hour,m)

def sending(msg,person,hour,m):
    try:

        person='+91'+person
        pywhatkit.sendwhatmsg(person,msg,hour,m,10)
        time.sleep(10)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('ctrl','w')
        pyautogui.hotkey('ctrl', 'shift', 'w')
        
    except:
        error="Error while sending msg"
        print(error)
        read_aloud(error)
        
def conversation_flow():
    with sr.Microphone() as source:
            intro="Nova is waiting for you."
            print(intro)
            read_aloud(intro)
            while True:
                audio = r.listen(source)
                start = r.recognize_google(audio)
                if "nova" in start.lower():
                    introduction()
                    while True:
                        text=("Speak to me, dearest. ")
                        print("Nova: "+str(text))
                        read_aloud(text)
                        audio = r.listen(source)
                        try:
                            print("You said: " + r.recognize_google(audio))
                            prompt = r.recognize_google(audio)
                        except sr.UnknownValueError:
                            error=("Google Speech Recognition could not understand audio")
                            time.sleep(1)
                            print(error)
                            read_aloud(error)
                            pass
                        except sr.RequestError as e:
                            error1=("Could not request results from Google Speech Recognition service; {0}".format(e))
                            time.sleep(1)
                            print(error1)
                            read_aloud(error1)
                            pass
                        print("You:", prompt)
                        if "quit" in prompt or "bye" in prompt or "shut up" in prompt or "go away" in prompt or "exit" in prompt or "farewell" in prompt:
                            print("Nova: "+"".join({em.emojize(':frowning_face:')}))
                            sys.exit()
            
                        if "capabilities" in prompt.lower() or "capability" in prompt.lower() or "abilities" in prompt.lower() or "you do" in prompt.lower():
                            text="I can generate prompts and show you weather forecast of any city. I can also send a whatsapp message too as well as play music for you."
                            print("Nova:",text)
                            read_aloud(text)
                            
                        elif "hello" in prompt.lower() or "hey" in prompt.lower() or "whats up" in prompt.lower() or "hi" in prompt.lower():
                            hello="Hey there good soul. I am Nova. I hope you have a nice day."
                            print("Nova:" + str(hello))
                            read_aloud(hello)
                        
                        elif "who" in prompt.lower():
                            response = model.generate_content(["You will generate answers within 75 tokens. Write in a continuous flow, avoiding bulleted lists." + prompt])
                            original=str(response.text)
                            new = original.replace("Gemini", "Nova").replace("developed","powered").replace("Google","Gemini")
                            print("Nova: "+ str(new))
                            read_aloud(new)
                        
                        elif "music" in prompt.lower() or "spotify" in prompt.lower() or "song" in prompt.lower() or "songs" in prompt.lower():
                            song="Connect and open spotify in your system"
                            print("Nova: "+str(song))
                            read_aloud(song)
                            time.sleep(3)
                            do="I will now search a song for you"
                            print("Nova: "+str(do))
                            read_aloud(do)
                            spo.search_play()
                            time.sleep(3)
                            inner_loop= True
                            while inner_loop:
                                options="I can play as well as pause the song. Tell disconnect to exit"
                                print("Nova: "+str(options))
                                read_aloud(options)
                                with sr.Microphone() as source4:
                                    audio = r.listen(source4)
                                    print("You said: " + r.recognize_google(audio))
                                    choose = r.recognize_google(audio)
                                    if "pause" in choose.lower() or "stop" in choose.lower():
                                        spo.pause()
                                    elif "play" in choose.lower() or "resume" in choose.lower() or "start" in choose.lower():
                                        spo.resume()
                                    elif "disconnect" in choose.lower() or "quit" in choose.lower() or "shut" in choose.lower():
                                        stop="You want the song to keep playing or stop playing"
                                        print("Nova: " + str(stop))
                                        read_aloud(stop)
                                        with sr.Microphone() as source4:
                                            audio = r.listen(source4)
                                            print("You said: " + r.recognize_google(audio))
                                            user = r.recognize_google(audio)
                                            if "stop" in user.lower():
                                                spo.pause()
                                                inner_loop=False
                                            else:
                                                inner_loop=False 

                        elif "weather" in prompt.lower() or "forecast" in prompt.lower() or "sky" in prompt.lower():
                            citytext="Do you want your city or some other, dearest. "
                            print("Nova: " + str(citytext))
                            read_aloud(citytext)
                            time.sleep(1)
                            with sr.Microphone() as source1:
                                audio = r.listen(source1)
                                print("You said: " + r.recognize_google(audio))
                                ans = r.recognize_google(audio)
                                if "yes" in ans.lower() or "my" in ans.lower() or "first" in ans.lower() :
                                    weather("Kolkata")
                                else:
                                    ask="Tell me your city, dearest."
                                    print("Nova:"+str(ask))
                                    read_aloud(ask)
                                    audio = r.listen(source1)
                                    print("You said: " + r.recognize_google(audio))
                                    weather_prompt = r.recognize_google(audio)
                                    weather(weather_prompt)
                                    
                        elif "whatsapp" in prompt.lower() or "message" in prompt.lower():
                            wapp="Dear, please login into your web whatsapp beforehand"
                            print("Nova:"+str(wapp))
                            read_aloud(wapp)
                            time.sleep(5)
                            no="Tell the number you want to message"
                            print("Nova:"+str(no))
                            read_aloud(no)
                            time.sleep(0.5)
                            with sr.Microphone() as source2:
                                audio = r.listen(source2)
                                print("You said: " + r.recognize_google(audio))
                                number = r.recognize_google(audio)
                                confirm="Are you sure"
                                print("Nova:"+str(confirm))
                                read_aloud(confirm)
                                audio = r.listen(source2)
                                print("You said: " + r.recognize_google(audio))
                                conf = r.recognize_google(audio)
                                if "yes" in conf.lower() or "ya" in conf.lower() or "yeah" in conf.lower():
                                    msg="Enter your message"
                                    read_aloud(msg)
                                    print("Nova:"+str(msg))
                                    audio = r.listen(source2)
                                    print("You said: " + r.recognize_google(audio))
                                    message = r.recognize_google(audio)
                                    send_msg(message,number)
                                    sent="I have sent your message"
                                    print("Nova:"+str(sent))
                                    read_aloud(sent)
                                else:
                                    pass
                                                                                                        
                        else:
                            generate(prompt)
                else:
                    pass
        

conversation_flow()
