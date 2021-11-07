import socket
import json
from random import *
# Alice
# Claimant


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    file = open("params.txt", "r")
    data = file.read()
    data_modif = json.loads(data)
    e = data_modif["e"]
    n = data_modif["n"]
    s = data_modif["s"]
    file.close()

    message = input(
        " Enter bye to exit or something else to start verification : ")  # take input

    while message.lower().strip() != 'bye':
        r = randint(1, n)
        x = pow(r, e, n)
        client_socket.send(str(x).encode())  # send witness
        # client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()  # receive challenge
        c = int(data)
        print('From Verifier Challenge: ' + str(c))
        y = (r * pow(s, c, n)) % n
        client_socket.send(str(y).encode())  # send response
        # print('Received from server: ' + data)  # show in terminal

        # again take input
        message = input(
            " Enter bye to exit or something else to start verification : ")

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
