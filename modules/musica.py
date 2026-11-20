import glob
import os
import tempfile
import webbrowser
from urllib.parse import quote_plus

# Tocamos o áudio pelo próprio Python (yt-dlp baixa, pygame toca), porque o
# navegador bloqueia vídeo que começa sozinho. Tudo instala com pip
# (veja requirements.txt): yt-dlp, imageio-ffmpeg e pygame.

PASTA_TEMP = os.path.join(tempfile.gettempdir(), 'assistente_musica')
_tocando = False


def _apagar_arquivos():
    for arquivo in glob.glob(os.path.join(PASTA_TEMP, 'musica_atual.*')):
        try:
            os.remove(arquivo)
        except OSError:
            pass


def _baixar_audio(termo):
    """Baixa o áudio do 1º resultado do YouTube como mp3. Devolve (titulo, caminho)."""
    import yt_dlp
    import imageio_ffmpeg  # traz o ffmpeg dentro do pacote, sem instalar programa

    os.makedirs(PASTA_TEMP, exist_ok=True)
    _apagar_arquivos()
    opcoes = {
        'quiet': True,
        'noprogress': True,
        'noplaylist': True,
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(PASTA_TEMP, 'musica_atual.%(ext)s'),
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        'postprocessors': [{'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3', 'preferredquality': '192'}],
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info('ytsearch1:' + termo, download=True)
    titulo = info['entries'][0].get('title', termo)
    return titulo, os.path.join(PASTA_TEMP, 'musica_atual.mp3')


def parar_musica(_=''):
    """Para a música que estiver tocando. Devolve texto."""
    global _tocando
    if not _tocando:
        return 'Não há música tocando'
    import pygame
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()  # solta o arquivo (o Windows não deixa apagar em uso)
    _apagar_arquivos()
    _tocando = False
    return 'Música parada'


def tocar_musica(termo):
    """Baixa e toca a música do YouTube, sem navegador. Devolve texto."""
    global _tocando
    termo = termo.strip()
    if not termo:
        return 'Qual música você quer ouvir?'
    parar_musica()  # só uma música por vez
    try:
        titulo, caminho = _baixar_audio(termo)
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()
        _tocando = True
        return 'Tocando ' + titulo
    except Exception as erro:  # pacote faltando, sem internet, etc.
        print('[musica] não consegui tocar:', erro)
        webbrowser.open('https://www.youtube.com/results?search_query=' + quote_plus(termo))
        return 'Não consegui tocar direto, abri a busca do YouTube para ' + termo


COMANDOS = [
    (['tocar musica', 'toque musica', 'toca musica', 'tocar', 'toque', 'toca',
      'colocar musica', 'coloque musica', 'coloca musica', 'reproduzir',
      'reproduza', 'quero ouvir', 'no youtube'], tocar_musica),
    (['parar musica', 'pare a musica', 'pare musica', 'para a musica',
      'parar a musica', 'pausar musica', 'pausar', 'pare', 'parar',
      'desligar musica', 'silencio'], parar_musica),
]
