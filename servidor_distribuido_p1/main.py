from connections.Connection import Connection
from model.Piso1 import Piso1
import sys

def main(json_file):
    server = Connection(Piso1(json_file))
    server.start()

if __name__ == "__main__":
    json_file = sys.argv[1]
    main(json_file)