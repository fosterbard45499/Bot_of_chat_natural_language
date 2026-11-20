import webbrowser
from urllib.parse import quote_plus


def pesquisar(termo):
    """Abre uma busca no Google com o que o usuário falou. Devolve texto."""
    termo = termo.strip()
    if not termo:
        return 'O que você quer pesquisar?'
    webbrowser.open('https://www.google.com/search?q=' + quote_plus(termo))
    return 'Pesquisando por ' + termo


# (gatilhos, função). A função recebe o resto da frase e devolve texto.
COMANDOS = [
    (['pesquisar por', 'pesquisar', 'pesquise por', 'pesquise', 'procure por',
      'procurar por', 'procure', 'busque por', 'buscar', 'busque',
      'googlar', 'no google'], pesquisar),
]
