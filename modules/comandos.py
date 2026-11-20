"""Junta o COMANDOS de cada módulo e despacha a frase para a função certa."""
from modules import pesquisa, musica
from modules.texto import normalizar

MODULOS = [pesquisa, musica]

# lista de (gatilho normalizado, função); gatilhos mais longos têm prioridade
COMANDOS = sorted(
    ((normalizar(g), fn) for m in MODULOS for gatilhos, fn in m.COMANDOS for g in gatilhos),
    key=lambda item: len(item[0]), reverse=True)


def executar(frase):
    """Recebe o que veio depois do nome da assistente.
    Devolve o texto a ser falado, ou None se nenhum comando bateu."""
    frase = normalizar(frase)
    for gatilho, fn in COMANDOS:
        if frase == gatilho or frase.startswith(gatilho + ' '):
            return fn(frase[len(gatilho):].strip())
    # gatilho no meio da frase (ex.: "me ajude a pesquisar gatos")
    cercada = ' ' + frase + ' '
    for gatilho, fn in COMANDOS:
        marca = ' ' + gatilho + ' '
        if marca in cercada:
            return fn(cercada.split(marca, 1)[1].strip())
    return None
