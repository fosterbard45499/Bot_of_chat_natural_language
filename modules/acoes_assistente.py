from datetime import datetime

from modules import carrega_agenda, comandos_respostas
from modules.data_portugues import data_em_portugues
from modules.lembretes import adicionar_lembrete, apagar_lembretes, listar_lembretes


PREFIXOS_PESQUISA = (
    "pesquisar no google",
    "pesquise no google",
    "pesquisar",
    "pesquise",
    "pesquisa",
    "buscar",
    "busque",
)


def extrair_comando_ativacao(frase, nome):
    frase = frase.strip()
    nome = nome.strip()
    if not frase.casefold().startswith(nome.casefold()):
        return None

    restante = frase[len(nome):]
    if restante and not (restante[0].isspace() or restante[0] in ",.!?:;"):
        return None
    return restante.lstrip(" ,.!?:;").strip().casefold()


def extrair_termo_pesquisa(comando):
    for prefixo in PREFIXOS_PESQUISA:
        if comando == prefixo:
            return ""
        if comando.startswith(f"{prefixo} "):
            return comando[len(prefixo):].strip()
    return None


def processar_comando(
    comando,
    falar,
    abrir_pesquisa=None,
    carregador_agenda=carrega_agenda.carrega_agenda,
    caminho_lembretes=None,
):
    comando = comando.strip().casefold().rstrip(" .!?")
    if not comando:
        return True

    if comando in ("encerrar", "sair", "fechar assistente"):
        falar("Até mais!")
        return False

    if comando in comandos_respostas.funcoes:
        falar("Até agora minhas funções são: " + comandos_respostas.funcionalidades)
    elif comando in comandos_respostas.data:
        falar(data_em_portugues())
    elif comando in comandos_respostas.horas:
        falar(f"Agora são {datetime.now():%H:%M}.")
    elif comando in comandos_respostas.apagar_lembretes:
        quantidade = apagar_lembretes(caminho_lembretes)
        falar("Lista de anotações apagada." if quantidade else "Você não tem anotações para apagar.")
    elif comando in comandos_respostas.ler_lembretes:
        lembretes = listar_lembretes(caminho_lembretes)
        falar("Você não tem anotações cadastradas." if not lembretes else "Suas anotações são: " + "; ".join(lembretes))
    elif comando in comandos_respostas.agenda:
        try:
            eventos = carregador_agenda()
        except FileNotFoundError:
            falar("Não encontrei a planilha agenda.xlsx. Coloque-a na pasta do projeto para consultar a agenda.")
        else:
            if not eventos:
                falar("Você não tem compromissos para hoje.")
            else:
                descricoes = [
                    f"{evento['hora']:%H:%M}: {evento['descricao']}, responsável {evento['responsavel']}"
                    for evento in eventos
                ]
                falar("Seus compromissos de hoje são: " + "; ".join(descricoes))
    else:
        termo_pesquisa = extrair_termo_pesquisa(comando)
        if termo_pesquisa is not None:
            if not termo_pesquisa:
                falar("Diga o que você quer pesquisar.")
            elif abrir_pesquisa is None:
                falar("A pesquisa no Google não está disponível.")
            else:
                abrir_pesquisa(termo_pesquisa)
        elif comando in comandos_respostas.ajuda:
            falar("Diga o que você quer pesquisar, por exemplo: pesquisar previsão do tempo.")
        else:
            prefixos_lembrete: list[str] = sorted(comandos_respostas.lembretes, key=len, reverse=True)
            for prefixo in prefixos_lembrete:
                if comando == prefixo:
                    falar("Inclua o texto no comando, por exemplo: anote comprar pão.")
                    break
                if comando.startswith(f"{prefixo} "):
                    texto = comando[len(prefixo):].strip()
                    adicionar_lembrete(texto, caminho_lembretes)
                    falar(f"Anotei: {texto}")
                    break
            else:
                falar("Não reconheci esse comando.")
    return True
