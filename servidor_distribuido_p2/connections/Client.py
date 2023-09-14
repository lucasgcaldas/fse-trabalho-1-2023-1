import socket
import json

class Client:
    def send_message(self, servidor_central, porta_central, data):
        central_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_conn.connect((servidor_central, porta_central))
        central_conn.send(json.dumps(data).encode())
        central_conn.close()