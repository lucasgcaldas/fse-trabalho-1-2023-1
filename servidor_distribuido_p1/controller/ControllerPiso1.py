from connections.Client import Client
from model.Piso1 import Piso1
import RPi.GPIO as GPIO
import threading

class ControllerPiso1(threading.Thread):
    def __init__(self, piso1: Piso1) -> None:
        super().__init__()
        self.piso1 = piso1
        self.vagas_ocupadas = [] # lista para armazenar as vagas ocupadas

    def abre_cancela_entrada(self, channel):
        print("abre entrada")
        self.piso1.abrir_cancela_entrada()
        data = {"message": "entrou_carro"}
        Client().send_message(self.piso1.servidor_central, self.piso1.porta_central, data)

    def fecha_cancela_entrada(self, channel):
        print("fecha entrada")
        self.piso1.fechar_cancela_entrada()

    def abre_cancela_saida(self, channel):
        print("abre saida")
        self.piso1.abrir_cancela_saida()
        data = {"message": "saiu_carro"}
        Client().send_message(self.piso1.servidor_central, self.piso1.porta_central, data)
    
    def fecha_cancela_saida(self, channel):
        print("fecha saida")
        self.piso1.fechar_cancela_saida()

    def estaciona_carro(self, channel):
        # verifica se o estado do pino do sensor de vaga mudou para 1
        if GPIO.input(self.piso1.sensor_vaga):
            # percorre a lista de saídas para encontrar a vaga que foi ocupada
            for i in range(len(self.piso1.output_values)):
                if self.piso1.output_values[i] == [GPIO.input(self.piso1.end_3), GPIO.input(self.piso1.end_2), GPIO.input(self.piso1.end_1)]:
                    if i+1 not in self.vagas_ocupadas: # verifica se a vaga já está ocupada
                        self.vagas_ocupadas.append(i+1) # adiciona a vaga na lista de vagas ocupadas
                        print(f"Vaga {i+1} foi ocupada.")
                        data = {"message": "estacionou_carro", "endereco": self.piso1.output_values[i]}
                        Client().send_message(self.piso1.servidor_central, self.piso1.porta_central, data)
                    break
        # else:
        #     print("Sensor de vaga voltou para 0.")
        #     data = {"message": "saiu_carro", "endereco": [self.piso1.end_3, self.piso1.end_2, self.piso1.end_1]}
        #     Client().send_message(self.piso1.servidor_central, self.piso1.porta_central, data)


    def sai_carro(self, channel):
        # verifica se o estado do pino do sensor de vaga mudou para 0
        if not GPIO.input(self.piso1.sensor_vaga):
            # percorre a lista de saídas para encontrar a vaga que foi desocupada
            for i in range(len(self.piso1.output_values)):
                if self.piso1.output_values[i] == [GPIO.input(self.piso1.end_3), GPIO.input(self.piso1.end_2), GPIO.input(self.piso1.end_1)]:
                    print(f"Vaga {i+1} foi desocupada.")
                    data = {"message": "saiu_carro", "endereco": self.piso1.output_values[i]}
                    Client().send_message(self.piso1.servidor_central, self.piso1.porta_central, data)
                    break 

    def run(self):
        # Configura os eventos para os sensores
        GPIO.add_event_detect(self.piso1.sensor_abertura_entrada, GPIO.RISING, callback=self.abre_cancela_entrada, bouncetime=200)
        GPIO.add_event_detect(self.piso1.sensor_fechamento_entrada, GPIO.RISING, callback=self.fecha_cancela_entrada, bouncetime=200)
        GPIO.add_event_detect(self.piso1.sensor_abertura_saida, GPIO.RISING, callback=self.abre_cancela_saida, bouncetime=200)
        GPIO.add_event_detect(self.piso1.sensor_fechamento_saida, GPIO.RISING, callback=self.fecha_cancela_saida, bouncetime=200)

        # registra o evento de mudança no estado do sensor de vaga de 0 para 1
        GPIO.add_event_detect(self.piso1.sensor_vaga, GPIO.RISING, callback=self.estaciona_carro)

        # registra o evento de mudança no estado do sensor de vaga de 1 para 0
#        GPIO.add_event_detect(self.piso1.sensor_vaga, GPIO.FALLING, callback=self.estaciona_carro)
