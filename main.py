import playsound3
import pyttsx3
import speech_recognition as sr
from playsound3 import playsound
import random
import datetime
hour = datetime.datetime.now().strftime('%H:%M')
#print(hour)
date = datetime.date.today().strftime('%d/%B/%Y')
#print(date)
date = date.split('/')
#print(date)
import webbrowser as wb
import tensorflow as tf
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from modules import carrega_agenda, comandos_respostas
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

# pesquisa
# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# Windows
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# Linux
# chrome_path = '/usr/bin/google-chrome %s'

def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)

search('o que fazer no feriado')


def speak(audio):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120) # número de palavras por minuto
    engine.setProperty('volume', 1) # min: 0, max: 1
    engine.say(audio)
    engine.runAndWait()

speak('Testando o sintetizador de voz da assistente')


def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=0.9)
        print('Ouvindo:')
        audio = microfone.listen(source)
        with open ('recordings/speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())
    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print('Você disse: ' + frase)
    except sr.UnknownValueError:
        frase = ''
        print('Não entendi')
    return frase

playing = False
mode_control = False
print('[INFO] Pronto para começar!')
playsound('n1.mp3')
meu_nome = 'Mocheng'

while (1):
    result = listen_microphone()

    if meu_nome in result:
        result = str(result.split(meu_nome + ' ')[1])
        result = result.lower()
        print('Acionou a assistente!')
        print('Após o processamento: ', result)

        # funcoes do assistente
        if result in comandos[0]:
            playsound('n2.mp3')
            speak('Até agora minhas funções são: ' + respostas[0])

        if result == 'encerrar':
            playsound('n2.mp3')
            speak(''.join(random.sample(respostas[4], k = 1)))
            break
        else:
            playsound('n3.mp3')
            speak('Ouvindo')

