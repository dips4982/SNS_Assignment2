import socket
from Crypto.Util.number import *
from random import *
from hashlib import sha1
import json


def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


def signing(message, p, q, d, e1, e2):
    # r is the random secret
    r = randint(2, p - 1)
    r_inverse = mod_inverse(r, q)
    hashed_message = sha1(message.encode("UTF-8")).hexdigest()
    hash_val = int(hashed_message, 16)
    s1 = (pow(e1, r) % p) % q
    s2 = ((hash_val+d*s1)*r_inverse) % q

    return r, s1, s2


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    file = open("params.txt", "r")
    contents = (file.read())
    content_modif = contents.split(" ")
    p = content_modif[0]
    q = content_modif[1]
    d = content_modif[2]
    e1 = content_modif[3]
    e2 = content_modif[4]
    file.close()

    message = input(
        " Enter a message to Bob to verify signature: ")  # take input

    while message.lower().strip() != 'bye':
        r, s1, s2 = signing(message, int(p), int(q), int(d), int(e1), int(e2))
        data = {"message": message, "s1": s1, "s2": s2}
        data_json = json.dumps(data)
        client_socket.send(data_json.encode())  # send message
        # client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        # again take input
        message = input(" Enter a message to Bob to verify signature: ")

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
