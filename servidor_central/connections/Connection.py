from connections.Client import Client
from model.Carro import Carro
import threading
import socket
import time
import json

class Connection(threading.Thread):
    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        # Cria um objeto de socket do tipo servidor
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.num_carros = 0
        self.carros = []
    
    def run(self) -> None:
        # Começa a escutar conexões de entrada em uma thread
        self.server_socket.listen()
        print(f"Servidor central - {self.host}:{self.port}")
        while True:
            try:
                # Aceita conexões de entrada
                client_socket, client_address = self.server_socket.accept()
                # print(f"Nova connexao de {client_socket} {client_address}")

                data = client_socket.recv(1024).decode()
                data_json = json.loads(data)

                if data_json["message"] == "scan_vagas_piso1" or data_json["message"] == "scan_vagas_piso2":
                    vagas = data_json["vagas"]
                    print(vagas)

                elif data_json["message"] == "entrou_carro":
                    carro = Carro()
                    self.carros.append(carro)
                    self.num_carros += 1
                    print(f"Total carros: {self.num_carros}")

                elif data_json["message"] == "estacionou_carro":
                    vaga = data_json["endereco"]
                    ultimo_carro = len(self.carros)
                    self.carros[ultimo_carro - 1].vaga = vaga
                    print(f"Token: {carro.token} - Entrada: {carro.tempo_entrada} - Vaga: {carro.vaga}")

                elif data_json["message"] == "saiu_carro":
                    vaga = data_json["endereco"]
                    for carro in self.carros:
                        if carro.vaga == vaga:
                            carro.calcula_preco_total()   
                            print(carro.to_string())
                            self.num_carros -= 1 
                            break

                if self.num_carros == 16:
                    data = {"message": "ativar_led_lotado"}
                    print("lotou_pisos")
                    # Envia a mensagem para o piso 1
                    Client().send_message_piso1(data)
                else:
                    data = {"message": "ainda_tem_vaga"}
                    print("ainda_tem_vaga")
                    # Envia a mensagem para o piso 1
                    Client().send_message_piso1(data)

                time.sleep(0.5)

            except Exception as erro:
                    print(f"Erro na conexão: {erro}")
                    time.sleep(0.5)
