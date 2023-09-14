import RPi.GPIO as GPIO
import time
import json

class Piso1:
    def __init__(self, filename: str) -> None:
        with open(f"configs/{filename}.json", "r") as f:
            file = json.load(f)

        json_outputs = file["outputs"]
        json_inputs = file["inputs"]

        self.servidor_central = file["host_servidor_central"]
        self.porta_central = file["port_servidor_central"]
        self.host = file["host"]
        self.port = file["port"]
        self.nome = file["nome"]

        for item in json_outputs:
            if item["tag"] == "ENDERECO_01":
                self.end_1 = item["gpio"]
            elif item["tag"] == "ENDERECO_02":
                self.end_2 = item["gpio"]
            elif item["tag"] == "ENDERECO_03":
                self.end_3 = item["gpio"]
            elif item["tag"] == "SINAL_DE_LOTADO_FECHADO":
                self.led_lotado = item["gpio"]
            elif item["tag"] == "MOTOR_CANCELA_ENTRADA":
                self.motor_cancela_entrada = item["gpio"]
            elif item["tag"] == "MOTOR_CANCELA_SAIDA":
                self.motor_cancela_saida = item["gpio"]

        for item in json_inputs:
            if item["tag"] == "SENSOR_DE_VAGA":
                self.sensor_vaga = item["gpio"]
            elif item["tag"] == "SENSOR_ABERTURA_CANCELA_ENTRADA":
                self.sensor_abertura_entrada = item["gpio"]
            elif item["tag"] == "SENSOR_FECHAMENTO_CANCELA_ENTRADA":
                self.sensor_fechamento_entrada = item["gpio"]
            elif item["tag"] == "SENSOR_ABERTURA_CANCELA_SAIDA":
                self.sensor_abertura_saida = item["gpio"]
            elif item["tag"] == "SENSOR_FECHAMENTO_CANCELA_SAIDA":
                self.sensor_fechamento_saida = item["gpio"]

        self.num_carros = 0 # inicia num_carros = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Cancela Entrada
        self.cancela_aberta_entrada = False
        
        GPIO.setup(self.sensor_abertura_entrada, GPIO.IN)
        GPIO.setup(self.sensor_fechamento_entrada, GPIO.IN)
        GPIO.setup(self.motor_cancela_entrada, GPIO.OUT) 

        GPIO.output(self.motor_cancela_entrada, GPIO.LOW) # inicia motor entrada em LOW

        # Cancela Saida
        self.cancela_aberta_saida = False
        
        GPIO.setup(self.sensor_abertura_saida, GPIO.IN)
        GPIO.setup(self.sensor_fechamento_saida, GPIO.IN)
        GPIO.setup(self.motor_cancela_saida, GPIO.OUT) 

        GPIO.output(self.motor_cancela_saida, GPIO.LOW) # inicia motor saida em LOW

        # Sinal de Lotado - Led
        GPIO.setup(self.led_lotado, GPIO.OUT)

        # Sensores de Vagas       
        GPIO.setup(self.end_1, GPIO.OUT)
        GPIO.setup(self.end_2, GPIO.OUT)
        GPIO.setup(self.end_3, GPIO.OUT)
        GPIO.setup(self.sensor_vaga, GPIO.IN)
        
        # Define os valores das vagas
        self.output_values = [[GPIO.LOW, GPIO.LOW, GPIO.LOW],    # 1
                            [GPIO.LOW, GPIO.LOW, GPIO.HIGH],     # 2
                            [GPIO.LOW, GPIO.HIGH, GPIO.LOW],     # 3
                            [GPIO.LOW, GPIO.HIGH, GPIO.HIGH],    # 4
                            [GPIO.HIGH, GPIO.LOW, GPIO.LOW],     # 5
                            [GPIO.HIGH, GPIO.LOW, GPIO.HIGH],    # 6
                            [GPIO.HIGH, GPIO.HIGH, GPIO.LOW],    # 7
                            [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]]   # 8

    def abrir_cancela_entrada(self):
        GPIO.output(self.motor_cancela_entrada, GPIO.HIGH)
        
    def fechar_cancela_entrada(self):        
        GPIO.output(self.motor_cancela_entrada, GPIO.LOW)

    def abrir_cancela_saida(self):              
        GPIO.output(self.motor_cancela_saida, GPIO.HIGH)
        
    def fechar_cancela_saida(self):
        GPIO.output(self.motor_cancela_saida, GPIO.LOW)

    def liga_led_lotado(self):
        GPIO.output(self.led_lotado, GPIO.HIGH)

    def apaga_led_lotado(self):
        GPIO.output(self.led_lotado, GPIO.LOW)

    def mostra_vagas(self):
        vagas_piso1 = ""
        total = 0
        
        for i in range(8):
            GPIO.output(self.end_3, self.output_values[i][0])
            GPIO.output(self.end_2, self.output_values[i][1])
            GPIO.output(self.end_1, self.output_values[i][2])
            time.sleep(0.2)
            sensor_vaga = GPIO.input(self.sensor_vaga)
            vagas_piso1 += f"{i + 1} - {sensor_vaga} "
        
        if sensor_vaga == 1:
                total += 1

        return total, vagas_piso1