from interface.Interface import Interface

def main():
    host = "localhost"
    port = 10971

    interface = Interface(host, port)
    interface.start()

if __name__ == "__main__":
    main()
