import json
from pathlib import Path


ARQUIVO_LEMBRETES = Path(__file__).resolve().parent.parent / "lembretes.json"


def adicionar_lembrete(texto, caminho=None):
    texto = texto.strip()
    if not texto:
        raise ValueError("O texto do lembrete não pode ficar vazio.")

    arquivo = Path(caminho) if caminho else ARQUIVO_LEMBRETES
    lembretes = listar_lembretes(arquivo)
    lembretes.append(texto)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(
        json.dumps(lembretes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return texto


def listar_lembretes(caminho=None):
    arquivo = Path(caminho) if caminho else ARQUIVO_LEMBRETES
    if not arquivo.exists():
        return []
    lembretes = json.loads(arquivo.read_text(encoding="utf-8"))
    if not isinstance(lembretes, list) or not all(isinstance(item, str) for item in lembretes):
        raise ValueError(f"Formato inválido no arquivo de lembretes: {arquivo}")
    return lembretes


def apagar_lembretes(caminho=None):
    arquivo = Path(caminho) if caminho else ARQUIVO_LEMBRETES
    quantidade = len(listar_lembretes(arquivo))
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text("[]", encoding="utf-8")
    return quantidade
