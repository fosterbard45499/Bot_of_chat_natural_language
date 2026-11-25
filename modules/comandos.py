"""Junta o COMANDOS de cada módulo e despacha a frase para a função certa."""
from modules import pesquisa, musica
from modules.acoes_assistente import processar_comando
from modules.texto import normalizar

MODULOS = [pesquisa, musica]

# lista de (gatilho normalizado, função); gatilhos mais longos têm prioridade
COMANDOS = sorted(
    ((normalizar(g), fn) for m in MODULOS for gatilhos, fn in m.COMANDOS for g in gatilhos),
    key=lambda item: len(item[0]), reverse=True)


def executar(frase):
    """Recebe o que veio depois do nome da assistente.
    Devolve o texto a ser falado pelo comando correspondente."""
    frase_original = frase
    frase_normalizada = normalizar(frase)
    for gatilho, fn in COMANDOS:
        if frase_normalizada == gatilho or frase_normalizada.startswith(gatilho + ' '):
            return fn(frase_normalizada[len(gatilho):].strip())
    # gatilho no meio da frase (ex.: "me ajude a pesquisar gatos")
    cercada = ' ' + frase_normalizada + ' '
    for gatilho, fn in COMANDOS:
        marca = ' ' + gatilho + ' '
        if marca in cercada:
            return fn(cercada.split(marca, 1)[1].strip())

    respostas = []
    processar_comando(frase_original, respostas.append)
    return respostas[0] if respostas else None
