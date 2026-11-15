from pathlib import Path
from urllib.parse import quote_plus
import webbrowser

import pyttsx3
import speech_recognition as sr
from playsound3 import playsound

from modules.acoes_assistente import extrair_comando_ativacao, processar_comando


NOME_ASSISTENTE = "Luana"


def speak(audio):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120) # número de palavras por minuto
    engine.setProperty('volume', 1) # min: 0, max: 1
    engine.say(audio)
    engine.runAndWait()

#speak('Testando')


def listen_microphone():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        reconhecedor.adjust_for_ambient_noise(source, duration=0.9)
        print("Ouvindo:")
        audio = reconhecedor.listen(source)

    pasta_gravacoes = Path(__file__).resolve().parent / "recordings"
    pasta_gravacoes.mkdir(parents=True, exist_ok=True)
    (pasta_gravacoes / "speech.wav").write_bytes(audio.get_wav_data())
    try:
        frase = reconhecedor.recognize_google(audio, language="pt-BR")
        print("Você disse: " + frase)
        return frase
    except sr.UnknownValueError:
        print("Não entendi.")
        return ""
    except sr.RequestError as erro:
        print(f"Não foi possível acessar o serviço de reconhecimento de voz: {erro}")
        return ""


def search(frase):
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(frase))


def main():
    print("[INFO] Pronto para começar!")
    audio_inicio = Path(__file__).resolve().parent / "n1.mp3"
    playsound(str(audio_inicio))
    while True:
        frase = listen_microphone()
        comando = extrair_comando_ativacao(frase, NOME_ASSISTENTE)
        if comando is None:
            continue
        if not processar_comando(comando, speak, abrir_pesquisa=search):
            break


if __name__ == "__main__":
    main()
