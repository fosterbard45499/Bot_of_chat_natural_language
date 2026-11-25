import pyttsx3
import speech_recognition as sr
#from playsound import playsound  # sons desativados por enquanto
import random
import datetime
import re
hour = datetime.datetime.now().strftime('%H:%M')
#print(hour)
date = datetime.date.today().strftime('%d/%B/%Y')
#print(date)
date = date.split('/')
#print(date)
#import webbrowser as wb  # a pesquisa agora fica em modules/pesquisa.py
#import tensorflow as tf
#import numpy as np  # sem uso por enquanto
#import librosa
#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set()

from modules import comandos_respostas
from modules import comandos as comandos_modulos  # despachante (pesquisa, música...)
from modules.texto import normalizar
comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

# Pesquisa fixa do início (desativada: agora pesquisamos o que o usuário falar)
# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# Windows
#chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
# Linux
# chrome_path = '/usr/bin/google-chrome %s'

#def search(frase):
#    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)

#search('o que fazer no feriado')

def speak(audio):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120) # número de palavras por minuto
    engine.setProperty('volume', 1) # min: 0, max: 1
    engine.say(audio)
    engine.runAndWait()

#speak('Testando')

def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=0.9)
        print('Ouvindo:')
        audio = microfone.listen(source)
        with open('recordings/speech.wav', 'wb') as f:
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
#playsound('n1.mp3')
meu_nome = 'luana'  # em minúsculas: a comparação abaixo ignora maiúsculas e acentos

while (1):
    frase = listen_microphone()
    ativacao = re.search(rf'\b{re.escape(meu_nome)}\b', frase, re.IGNORECASE)

    if ativacao:
        result = frase[ativacao.end():].strip(' \t\r\n,.;:!?')
        result_normalizado = normalizar(result)
        print('Acionou a assistente!')
        print('Após o processamento: ', result)

        # funcoes do assistente
        if result_normalizado in [normalizar(c) for c in comandos[0]]:
            #playsound('n2.mp3')
            speak('Até agora minhas funções são: ' + respostas[0])

        elif result_normalizado in ('encerrar', 'sair', 'fechar assistente'):
            #playsound('n2.mp3')
            speak(''.join(random.sample(respostas[4], k = 1)))
            break

        elif result_normalizado == '':  # só disseram o nome
            speak(''.join(random.sample(respostas[2], k = 1)))

        else:
            # O despachante encaminha pesquisa/música e também os comandos principais.
            resposta = comandos_modulos.executar(result)
            #playsound('n3.mp3')
            speak(resposta if resposta else 'Não reconheci esse comando.')
