import RPi.GPIO as GPIO
import time
import json

class Piso2:
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

        for item in json_inputs:
            if item["tag"] == "SENSOR_DE_VAGA":
                self.sensor_vaga = item["gpio"]
            elif item["tag"] == "SENSOR_DE_PASSAGEM_1":
                self.sensor_passagem1 = item["gpio"]
            elif item["tag"] == "SENSOR_DE_PASSAGEM_2":
                self.sensor_passagem2 = item["gpio"]

        self.num_carros = 0 # inicia num_carros = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.sensor_passagem1, GPIO.IN)
        GPIO.setup(self.sensor_passagem2, GPIO.IN)

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

    def liga_led_lotado(self):
        GPIO.output(self.led_lotado, GPIO.HIGH)

    def apaga_led_lotado(self):
        GPIO.output(self.led_lotado, GPIO.LOW)

    def mostra_vagas(self):
        vagas_piso2 = ""
        total = 0

        for i in range(8):
            GPIO.output(self.end_3, self.output_values[i][0])
            GPIO.output(self.end_2, self.output_values[i][1])
            GPIO.output(self.end_1, self.output_values[i][2])
            time.sleep(0.2)
            sensor_vaga = GPIO.input(self.sensor_vaga)
            vagas_piso2 += f"{i + 9} - {sensor_vaga} "
            if sensor_vaga == 1:
                total += 1
            
        if total >= 8:
            self.liga_led_lotado()
        else:
            self.apaga_led_lotado()
        # print(vagas_piso2)
        return total, vagas_piso2