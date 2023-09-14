from model.Piso2 import Piso2
from connections.Client import Client
import RPi.GPIO as GPIO
import threading
import time
import json

class ControllerPiso2(threading.Thread):
    def __init__(self, piso2: Piso2) -> None:
        super().__init__()
        self.piso2 = piso2

    def estado_vaga(self, channel):
        # verifica se o estado do pino do sensor de vaga mudou para 1
        if GPIO.input(self.piso2.sensor_vaga):
            # percorre a lista de saídas para encontrar a vaga que foi ocupada
            for i in range(len(self.piso2.output_values)):
                if self.piso2.output_values[i] == [GPIO.input(self.piso2.end_3), GPIO.input(self.piso2.end_2), GPIO.input(self.piso2.end_1)]:
                    print(f"Vaga {i+1} foi ocupada.")
                    data = {"message": "estacionou_carro", "endereco": self.piso2.output_values[i]}
                    Client().send_message(self.piso2.servidor_central, self.piso2.porta_central, data)
                    break 
        else:
            # percorre a lista de saídas para encontrar a vaga que foi desocupada
            for i in range(len(self.piso2.output_values)):
                if self.piso2.output_values[i] == [GPIO.input(self.piso2.end_3), GPIO.input(self.piso2.end_2), GPIO.input(self.piso2.end_1)]:
                    print(f"Vaga {i+1} foi desocupada.")
                    data = {"message": "saiu_carro", "endereco": self.piso2.output_values[i]}
                    Client().send_message(self.piso2.servidor_central, self.piso2.porta_central, data)
                    break 

    def sai_carro(self, channel):
        # verifica se o estado do pino do sensor de vaga mudou para 0
        if not GPIO.input(self.piso2.sensor_vaga):
            # percorre a lista de saídas para encontrar a vaga que foi desocupada
            for i in range(len(self.piso2.output_values)):
                if self.piso2.output_values[i] == [GPIO.input(self.piso2.end_3), GPIO.input(self.piso2.end_2), GPIO.input(self.piso2.end_1)]:
                    print(f"Vaga {i+1} foi desocupada.")
                    data = {"message": "saiu_carro", "endereco": self.piso2.output_values[i]}
                    Client().send_message(self.piso2.servidor_central, self.piso2.porta_central, data)
                    break 

    def run(self):
        # registra o evento de mudança no estado do sensor de vaga de 0 para 1
        GPIO.add_event_detect(self.piso2.sensor_vaga, GPIO.BOTH, callback=self.estado_vaga)