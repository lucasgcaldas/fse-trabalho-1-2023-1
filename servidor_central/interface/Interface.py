from connections.Connection import Connection
from connections.Client import Client
import threading
#import reset
import sys


class Interface(threading.Thread):
    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.connection = Connection(host, port)

    def run(self):
        self.connection.start()
        while True:
            print('''
            1. Liga led lotado Piso 1
            2. Liga led lotado Piso 2
            3. Desliga led lotado Piso 1
            4. Desliga leds lotado Piso 2
            5. Lista carros
            6. Sair
            ''')

            choice = input()

            if choice == '1':
                data = {"message": "ativar_led_lotado"}
                # Envia a mensagem para o piso 1
                Client().send_message_piso1(data)
            elif choice == '2':
                data = {"message": "ativar_led_lotado"}
                # Envia a mensagem para o piso 1
                Client().send_message_piso2(data)
            elif choice == '3':
                data = {"message": "desativar_led_lotado"}
                # Envia a mensagem para o piso 1
                Client().send_message_piso1(data)
            elif choice == '4':
                data = {"message": "desativar_led_lotado"}
                # Envia a mensagem para o piso 1
                Client().send_message_piso2(data)
            elif choice == '5':
                for carro in self.connection.carros:
                    print(carro.token, carro.tempo_entrada, carro.vaga)
            else:
                print("Fechando servidor central...")
                sys.exit()
