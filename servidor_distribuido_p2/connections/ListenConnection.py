from controller.ControllerPiso2 import ControllerPiso2
from connections.Client import Client
from model.Piso2 import Piso2
import RPi.GPIO as GPIO
import threading
import socket
import time
import json

class ListenConnection(threading.Thread):
    def __init__(self, piso2: Piso2) -> None:
        super().__init__()
        self.controller_piso2 = ControllerPiso2(piso2)
        self.host = self.controller_piso2.piso2.host
        self.port = self.controller_piso2.piso2.port
        self.servidor_central = self.controller_piso2.piso2.servidor_central
        self.porta_central = self.controller_piso2.piso2.porta_central
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def run(self):
        self.server_socket.listen()
        while True:
            try:
                # Aceita conexões de entrada
                client_socket, client_address = self.server_socket.accept()
                # print(f"Nova connexao de {client_socket} {client_address}")

                data = client_socket.recv(1024).decode()
                data_json = json.loads(data)

                if data_json["message"] == "ativar_led_lotado":
                    self.controller_piso2.piso2.liga_led_lotado()
                
                if data_json["message"] == "desativar_led_lotado":
                    self.controller_piso2.piso2.apaga_led_lotado()

                time.sleep(0.1)
            except Exception as erro:
                    print(f"Erro na conexão: {erro}")
                    time.sleep(0.5)