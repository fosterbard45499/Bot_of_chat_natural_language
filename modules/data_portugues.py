from datetime import date


MESES = (
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
)


def data_em_portugues(data=None):
    data = data or date.today()
    dia = f"{data.day}º" if data.day == 1 else str(data.day)
    return f"{dia} de {MESES[data.month - 1]} de {data.year}"
