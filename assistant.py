import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import pyaudio
import wave
import pyglet
import playsound
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

app = Flask(__name__)
api = Api(app)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
FRAMES = []
P = pyaudio.PyAudio()

CORS(app)


@app.route("/")
def hello():
    speak('Hello Sir, I am your digital assistant')
    greetMe()
    speak('How may I help you?')

    # stream = P.open(format=FORMAT,
    #                 channels=CHANNELS,
    #                 rate=RATE,
    #                 input=True,
    #                 frames_per_buffer=CHUNK)

    # print("* recording")

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    #     # print(type(frames))

    while True:

        query = myCommand()
        query = query.lower()

        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!',
                      'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'me' in recipient:
                try:
                    speak('What should I say? ')
                    content = myCommand()

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("bsss.3332@gmail.com", 'vinayak2015')
                    server.sendmail('Shubham', "Vivek", content)
                    server.close()
                    speak('Email sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')

        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            print("* done recording")
            stream.stop_stream()
            stream.close()
            p.terminate()
            sys.exit()

        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(P.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(FRAMES))
            wf.close()
            sys.exit()

        elif 'play music' in query:
            music_folder = 'D:\CodeCombat\mp3Songs'
            music = ['\R', '\W', '\A']
            random_music = music_folder + random.choice(music) + '.mp3'
            speak('Okay, here is your music! Enjoy!')
            os.system(random_music)

        else:
            query = query
            # speak('Searching...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)

            except:
                webbrowser.open('www.google.com')

        speak('Next Command! Sir!')

    return jsonify({'text': 'Hello World!'})


engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('THE87U-AXRX25RYLE')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)


def speak(audio):
    print('Computer: ' + audio)
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 16:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH != 0:
        speak('Good Evening!')


def myCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        FRAMES.append(audio.frame_data)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        # print(dir(audio))

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query


if __name__ == '__main__':
     app.run(port=5002)


# if __name__ == '__main__':

    # while True:

    #     query = myCommand();
    #     query = query.lower()

    #     if 'open youtube' in query:
    #         speak('okay')
    #         webbrowser.open('www.youtube.com')

    #     elif 'open google' in query:
    #         speak('okay')
    #         webbrowser.open('www.google.co.in')

    #     elif 'open gmail' in query:
    #         speak('okay')
    #         webbrowser.open('www.gmail.com')

    #     elif "what\'s up" in query or 'how are you' in query:
    #         stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
    #         speak(random.choice(stMsgs))

    #     elif 'email' in query:
    #         speak('Who is the recipient? ')
    #         recipient = myCommand()

    #         if 'me' in recipient:
    #             try:
    #                 speak('What should I say? ')
    #                 content = myCommand()

    #                 server = smtplib.SMTP('smtp.gmail.com', 587)
    #                 server.ehlo()
    #                 server.starttls()
    #                 server.login("Your_Username", 'Your_Password')
    #                 server.sendmail('Your_Username', "Recipient_Username", content)
    #                 server.close()
    #                 speak('Email sent!')

    #             except:
    #                 speak('Sorry Sir! I am unable to send your message at this moment!')

    #     elif 'nothing' in query or 'abort' in query or 'stop' in query:
    #         speak('okay')
    #         speak('Bye Sir, have a good day.')
    #         sys.exit()

    #     elif 'hello' in query:
    #         speak('Hello Sir')

    #     elif 'bye' in query:
    #         speak('Bye Sir, have a good day.')
    #         sys.exit()

    #     elif 'play music' in query:
    #         music_folder = Your_music_folder_path
    #         music = [music1, music2, music3, music4, music5]
    #         random_music = music_folder + random.choice(music) + '.mp3'
    #         os.system(random_music)

    #         speak('Okay, here is your music! Enjoy!')

    #     else:
    #         query = query
    #         # speak('Searching...')
    #         try:
    #             try:
    #                 res = client.query(query)
    #                 results = next(res.results).text
    #                 # speak('WOLFRAM-ALPHA says - ')
    #                 # speak('Got it.')
    #                 speak(results)

    #             except:
    #                 results = wikipedia.summary(query, sentences=2)
    #                 speak('Got it.')
    #                 speak('WIKIPEDIA says - ')
    #                 speak(results)

    #         except:
    #             webbrowser.open('www.google.com')

    #     speak('Next Command! Sir!')
