import re
import unicodedata


def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação, para comparar frases."""
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return re.sub(r'\s+', ' ', texto).strip()
