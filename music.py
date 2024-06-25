import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import os
from google.cloud import texttospeech_v1
import winsound 
import speech_recognition as sr

r = sr.Recognizer()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path-to-your-api-key'

client = texttospeech_v1.TextToSpeechClient()

client_id= 'your-client-id'
client_secret= 'your-client-secret'
redirect_uri = 'your-redirect-api'

sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=['user-read-playback-state', 'user-modify-playback-state', 'streaming','user-library-read'])
sp=spotipy.Spotify(auth_manager=sp_oauth)

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

def search_play():
    search="Tell me the name of the song you want to search for"
    print("Nova: "+ str(search))
    read_aloud(search)
    with sr.Microphone() as source:
        audio = r.listen(source)
        song = r.recognize_google(audio)
        results = sp.search(q=song, limit=1, type='track')
        print("You said: " + str(song))
        for i, t in enumerate(results['tracks']['items']):
            print(f"{i+1}. {t['name']} - {t['artists'][0]['name']}")
        ask="Are you sure"
        print("Nova: "+str(ask))
        read_aloud(ask)
        audio = r.listen(source)
        choice = r.recognize_google(audio)
        if "yes" in choice.lower() or "definitely" in choice.lower() or "yeah" in choice.lower() :
            track_id = results['tracks']['items'][0]['id']
            sp.start_playback(uris=[])
            play="Playing your song"
            print("Nova: " + str(play))
            read_aloud(play)
            sp.start_playback(uris=['spotify:track:' + track_id])
            track = sp.track(track_id)
            name = track['name']
            artist = track['artists'][0]['name']
            s_name="Name of the song is"
            s_artist="It is sung by"
            speak_song= str(s_name) + str(name)
            print("Nova: " + str(s_name) + " " + str(name))
            read_aloud(speak_song)
            speak_artist= str(s_artist) + str(artist)
            read_aloud(speak_artist)
            print("Nova: " + str(s_artist) + " " + str(artist))
        
        else:
            text="Better luck next time,dear"
            print("Nova: "+ str(text))
            read_aloud(text)

def pause():
    sp.pause_playback()
    pause="Song paused"
    print("Nova: "+str(pause))
    read_aloud(pause)

def resume():
    sp.start_playback()
    play="Song resumed"
    print("Nova: "+str(play))
    read_aloud(play)
    


