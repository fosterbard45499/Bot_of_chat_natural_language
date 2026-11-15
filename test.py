import tempfile
import unittest
from datetime import date, datetime, time, timedelta
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from modules.acoes_assistente import extrair_comando_ativacao, processar_comando
from modules.carrega_agenda import carrega_agenda
from modules.data_portugues import data_em_portugues
from modules.lembretes import adicionar_lembrete, apagar_lembretes, listar_lembretes


class DataEmPortuguesTests(unittest.TestCase):
    def test_formata_data_com_mes_em_portugues(self):
        self.assertEqual(data_em_portugues(date(2026, 11, 13)), "13 de novembro de 2026")

    def test_formata_primeiro_dia_com_ordinal(self):
        self.assertEqual(data_em_portugues(date(2026, 1, 1)), "1º de janeiro de 2026")


class LembretesTests(unittest.TestCase):
    def test_adiciona_e_lista_lembretes_persistidos(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "lembretes.json"
            adicionar_lembrete("  comprar pão  ", caminho)
            adicionar_lembrete("ligar para Ana", caminho)
            self.assertEqual(listar_lembretes(caminho), ["comprar pão", "ligar para Ana"])

    def test_rejeita_lembrete_vazio(self):
        with self.assertRaises(ValueError):
            adicionar_lembrete("  ", Path("lembretes.json"))

    def test_apaga_todos_os_lembretes(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "lembretes.json"
            adicionar_lembrete("comprar pão", caminho)
            adicionar_lembrete("ligar para Ana", caminho)

            self.assertEqual(apagar_lembretes(caminho), 2)
            self.assertEqual(listar_lembretes(caminho), [])

    def test_comandos_de_voz_criam_e_leem_anotacoes(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "lembretes.json"
            falas = []
            processar_comando("anote comprar pão", falas.append, caminho_lembretes=caminho)
            processar_comando("ler minhas anotações", falas.append, caminho_lembretes=caminho)
            self.assertIn("Anotei: comprar pão", falas)
            self.assertIn("Suas anotações são: comprar pão", falas)

    def test_comando_de_voz_apaga_a_lista_de_anotacoes(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "lembretes.json"
            adicionar_lembrete("comprar pão", caminho)
            falas = []

            processar_comando(
                "apagar a lista de anotações",
                falas.append,
                caminho_lembretes=caminho,
            )

            self.assertEqual(falas, ["Lista de anotações apagada."])
            self.assertEqual(listar_lembretes(caminho), [])


class AgendaTests(unittest.TestCase):
    def test_retorna_apenas_compromissos_de_hoje_ainda_pendentes(self):
        agora = datetime(2026, 11, 13, 14, 0)
        tabela = pd.DataFrame([
            {"data": agora.date(), "hora": time(13, 30), "descricao": "Passado", "responsavel": "Ana"},
            {"data": agora.date(), "hora": time(14, 30), "descricao": "Reunião", "responsavel": "Bia"},
            {"data": agora.date() + timedelta(days=1), "hora": time(15, 0), "descricao": "Amanhã", "responsavel": "Caio"},
        ])
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "agenda.xlsx"
            caminho.touch()
            with patch("modules.carrega_agenda.pd.read_excel", return_value=tabela):
                eventos = carrega_agenda(caminho, agora)

        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["descricao"], "Reunião")
        self.assertEqual(eventos[0]["responsavel"], "Bia")
        self.assertEqual(eventos[0]["hora"], time(14, 30))

    def test_informa_quando_planilha_nao_existe(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "ausente.xlsx"
            with self.assertRaises(FileNotFoundError):
                carrega_agenda(caminho)


class ComandosTests(unittest.TestCase):
    def test_ativacao_ignora_diferenca_de_maiusculas(self):
        self.assertEqual(extrair_comando_ativacao("MOCHENG, qual é a data?", "Mocheng"), "qual é a data?")

    def test_nao_ativa_quando_nome_aparece_dentro_de_outra_palavra(self):
        self.assertIsNone(extrair_comando_ativacao("Mochengue, agenda", "Mocheng"))

    @patch("modules.acoes_assistente.data_em_portugues", return_value="13 de novembro de 2026")
    def test_comando_de_data_fala_data_formatada(self, _mock_data):
        falas = []
        processar_comando("que dia é hoje", falas.append)
        self.assertEqual(falas, ["13 de novembro de 2026"])

    def test_comando_de_agenda_fala_eventos(self):
        falas = []
        eventos = [{"hora": time(14, 30), "descricao": "Reunião", "responsavel": "Bia"}]
        processar_comando("agenda", falas.append, carregador_agenda=lambda: eventos)
        self.assertEqual(falas, ["Seus compromissos de hoje são: 14:30: Reunião, responsável Bia"])

    def test_comando_de_pesquisa_envia_termo_ao_google(self):
        pesquisas = []
        processar_comando("pesquisar receita de bolo", lambda _: None, abrir_pesquisa=pesquisas.append)
        self.assertEqual(pesquisas, ["receita de bolo"])

    def test_pesquisa_sem_termo_pede_consulta(self):
        falas = []
        processar_comando("pesquisar", falas.append, abrir_pesquisa=lambda _: None)
        self.assertEqual(falas, ["Diga o que você quer pesquisar."])


if __name__ == "__main__":
    unittest.main()
