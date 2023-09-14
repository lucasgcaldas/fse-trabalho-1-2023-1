from connections.ListenConnection import ListenConnection
from controller.ControllerPiso1 import ControllerPiso1
from connections.Client import Client
from model.Piso1 import Piso1
import threading
import time

class Connection(threading.Thread):
    def __init__(self, piso1: Piso1) -> None:
        super().__init__()
        self.controller_piso1 = ControllerPiso1(piso1)
        self.listen_connection = ListenConnection(piso1)
        self.host = self.controller_piso1.piso1.host
        self.port = self.controller_piso1.piso1.port
        self.servidor_central = self.controller_piso1.piso1.servidor_central
        self.porta_central = self.controller_piso1.piso1.porta_central

    def run(self):
        self.controller_piso1.start()
        self.listen_connection.start()
        print(f"{self.controller_piso1.piso1.nome} - {self.host}:{self.port}")
        while True:
            try:
                # Envia a resposta para o servidor central
                total_piso1, vagas = self.controller_piso1.piso1.mostra_vagas()
                data = {"message": "scan_vagas_piso1", "vagas": F"Piso 1: {total_piso1} | {vagas}"}
                Client().send_message(self.servidor_central, self.porta_central, data)

                time.sleep(0.1)
            except Exception as erro:
                    print(f"Erro na conexão: {erro}")
                    time.sleep(0.5)