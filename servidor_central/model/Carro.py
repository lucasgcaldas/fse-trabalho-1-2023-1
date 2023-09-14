import datetime
import uuid

class Carro:
    def __init__(self) -> None:
        self.token = str(uuid.uuid4())[:4]
        self.tempo_entrada = datetime.datetime.now()
        self.tempo_saida = None
        self.vaga = None
        self.preco_total = None

    def calcula_preco_total(self):
        self.tempo_saida = datetime.datetime.now()
        diferenca_tempo = (self.tempo_entrada - self.tempo_saida).total_seconds() / 60
        self.preco_total = 0.15 * diferenca_tempo

    def to_string(self):
        f"Carro: {self.token} - Vaga: {self.vaga} - Entrada: {self.tempo_entrada} - Saida: {self.tempo_saida} - R$ {self.preco_total}"