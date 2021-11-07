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


def verifying(message, p, q, e1, e2, s1, s2):
    hashed_message = sha1(message.encode("UTF-8")).hexdigest()
    hash_val = int(hashed_message, 16)
    s2_inverse = mod_inverse(s2, q)

    w = mod_inverse(s1, q)
    # u1 = (hash_val * w) % q
    # u2 = (r * w) % q
    v = ((pow(e1, (hash_val*s2_inverse) % q) *
         pow(e2, (s1*s2_inverse) % q)) % p) % q
    if v == s1:
        # print("Valid Signature")
        return True
    else:
        # print("Invalid Signature")
        return False


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    file = open("params.txt", "r")
    contents = (file.read())
    content_modif = contents.split(" ")
    p = content_modif[0]
    q = content_modif[1]
    d = content_modif[2]
    e1 = content_modif[3]
    e2 = content_modif[4]
    file.close()

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        data_modif = json.loads(data)
        message = data_modif["message"]
        s1 = data_modif["s1"]
        s2 = data_modif["s2"]
        is_valid = verifying(message, int(p), int(
            q), int(e1), int(e2), int(s1), int(s2))
        if(is_valid):
            print("Valid Signature")
            print("from connected user: " + str(message))
            conn.send("Valid Signature".encode())
        else:
            print("Invalid Signature")
            conn.send("Invalid Signature".encode())

        # print("from connected user: " + str(message))
        # data = input(' -> ')
        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
