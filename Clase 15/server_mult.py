#!/usr/bin/python3
import socket
import multiprocessing
import sys

def child_process(connection):
    print("Initiating child process...\n")
    sock, addr = connection

    while True:
        message = sock.recv(1024)
        if message.decode() == '\r\n':
            continue
        else:
            data = message.decode()
            print("Received: %s from %s" % (message, addr))
            if data == "exit\r\n":
                reply = "\nFarewell\r\n".encode("utf-8")
                sock.send(reply)
                print("Client %s closed the connection\r\n" % str(addr))
                break
            else:
                reply_msg = data.upper() + "\r\n"
                sock.send(reply_msg.encode("utf-8"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_address = ""
listening_port = 50001

server_socket.bind((host_address, listening_port))
server_socket.listen(5)

while True:
    client = server_socket.accept()

    client_socket, client_address = client

    print("Connected to %s" % str(client_address))

    initial_msg = 'Thanks for connecting' + "\r\n"
    client_socket.send(initial_msg.encode('ascii'))

    child_proc = multiprocessing.Process(target=child_process, args=(client,))
    child_proc.start()

    client_socket.close()
