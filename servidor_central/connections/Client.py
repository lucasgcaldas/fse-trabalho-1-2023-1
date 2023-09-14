import socket
import json

class Client:
    def send_message_piso1(self, data):
        central_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_conn.connect(("localhost", 10972))
        central_conn.send(json.dumps(data).encode())
        central_conn.close()

    def send_message_piso2(self, data):
        central_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_conn.connect(("localhost", 10973))
        central_conn.send(json.dumps(data).encode())
        central_conn.close()