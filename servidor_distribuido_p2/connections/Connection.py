from connections.ListenConnection import ListenConnection
from controller.ControllerPiso2 import ControllerPiso2
from connections.Client import Client
from model.Piso2 import Piso2
import threading
import time

class Connection(threading.Thread):
    def __init__(self, piso2: Piso2) -> None:
        super().__init__()
        self.controller_piso2 = ControllerPiso2(piso2)
        self.listen_connection = ListenConnection(piso2)
        self.host = self.controller_piso2.piso2.host
        self.port = self.controller_piso2.piso2.port
        self.servidor_central = self.controller_piso2.piso2.servidor_central
        self.porta_central = self.controller_piso2.piso2.porta_central

    def run(self):
        # self.controller_piso2.start()
        self.listen_connection.start()
        print(f"{self.controller_piso2.piso2.nome} - {self.host}:{self.port}")
        while True:
            try:
                # Envia a resposta para o servidor central
                total_piso2, vagas = self.controller_piso2.piso2.mostra_vagas()
                data = {"message": "scan_vagas_piso2", "vagas": F"Piso 2: {total_piso2} | {vagas}"}
                Client().send_message(self.servidor_central, self.porta_central, data)

                time.sleep(0.1)
            except Exception as erro:
                    print(f"Erro na conexão: {erro}")
                    time.sleep(0.5)