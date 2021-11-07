import socket
from random import *
import json
# Bob

# Verifier


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    file = open("params.txt", "r")
    data = file.read()
    data_modif = json.loads(data)
    e = data_modif["e"]
    n = data_modif["n"]
    v = data_modif["v"]
    file.close()

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        x = int(data)
        print("from Claimant witness: " + str(x))
        c = randint(1, e)

        # print("from connected user: " + str(data))
        # data = input(' -> ')
        conn.send(str(c).encode())  # send challenge
        data = conn.recv(1024).decode()  # get response
        print('From Claimant Response : ' + data)
        y = int(data)
        verif = pow(y, e, n)*pow(v, c, n) % n
        print('Value of x : ' + str(x))
        print('Value of pow(y,e)*pow(v,c) : ' + str(verif))
        if(verif == x):
            print("Probable")
        else:
            print("Improbable")

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
