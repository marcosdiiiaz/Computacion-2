#!/usr/bin/python3
import socket
import threading

def worker_thread(connection):
    print("Initializing worker thread...")

    while True:
        data = connection.recv(1024)
        if data.decode() == '\r\n':
            continue
        else:
            message = data.decode()
            print("Received data: %s" % message)
            if message == "exit\r\n":
                response = "\nFarewell!\r\n".encode("utf-8")
                connection.send(response)
                print("The client terminated the link.\r\n")
                connection.close()
                break
            else:
                response_msg = message.upper() + "\r\n"
                connection.send(response_msg.encode("utf-8"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_address = ""
listening_port = 50001

server_socket.bind((host_address, listening_port))
server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()

    print("Connected to %s" % str(client_address))

    initial_msg = 'Appreciate your connection' + "\r\n"
    client_socket.send(initial_msg.encode('ascii'))

    worker = threading.Thread(target=worker_thread, args=(client_socket,))
    worker.start()
