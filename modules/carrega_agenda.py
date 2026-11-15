from datetime import datetime, time
from pathlib import Path

import pandas as pd


def carrega_agenda(caminho=None, agora=None):
    """Retorna os compromissos de hoje que ainda não aconteceram."""
    planilha = Path(caminho) if caminho else Path(__file__).resolve().parent.parent / "agenda.xlsx"
    if not planilha.is_file():
        raise FileNotFoundError(f"Planilha de agenda não encontrada: {planilha}")

    agora = agora or datetime.now()
    agenda = pd.read_excel(planilha)
    colunas = {"data", "hora", "descricao", "responsavel"}
    faltantes = colunas.difference(agenda.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes na planilha de agenda: {', '.join(sorted(faltantes))}")

    eventos = []
    for _, linha in agenda.iterrows():
        data_evento = pd.to_datetime(linha["data"]).date()
        valor_hora = linha["hora"]
        if isinstance(valor_hora, datetime):
            hora_evento = valor_hora.time()
        elif isinstance(valor_hora, time):
            hora_evento = valor_hora
        else:
            hora_evento = pd.to_datetime(str(valor_hora)).time()

        if data_evento == agora.date() and hora_evento >= agora.time():
            eventos.append({
                "descricao": str(linha["descricao"]),
                "responsavel": str(linha["responsavel"]),
                "hora": hora_evento,
            })
    return eventos
