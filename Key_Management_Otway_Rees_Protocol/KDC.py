import socket
from Crypto.Cipher import DES
from secrets import token_bytes
import os
import json
from Crypto.Util.Padding import pad, unpad

file = open("OR_params.txt", "r")
data = file.read()
data_modif = json.loads(data)
ka = bytes.fromhex(data_modif["ka"])
kb = bytes.fromhex(data_modif["kb"])
R = data_modif["R"]
file.close()

temp_R = R

Alice_name = "Alice"
Bob_name = "Bob"


def encrypt(msg, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(msg)
    return ciphertext


def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


def Encryption(data, key):
    data = pad(data, DES.block_size)
    ciphertext = encrypt(data, key)
    return ciphertext


def Decryption(ciphertext, key):
    plaintext = decrypt(ciphertext, key)
    return plaintext


def get_socket(port):
    s = socket.socket()
    s.connect(("127.0.0.1", port))
    return s


def bind_socket(port):
    s = socket.socket()
    s.bind(("", port))
    s.listen(5)
    return s

# port alice = 12345
# port bob = 12346
# port kdc = 12347


s = bind_socket(12347)
conn, addr = s.accept()
# from KDC
to_KDC = conn.recv(1024).decode()
# print(data)
file = open("execution_order.txt", "a")
file.write("From Bob to KDC 2\n")
file.write("" + to_KDC + "\n")
file.write("\n")
file.close()
to_KDC = json.loads(to_KDC)
Alice_string_PT = Decryption(bytes.fromhex(to_KDC["Alice_string_cipher"]), ka)
Alice_string_PT = unpad(Alice_string_PT, DES.block_size)
Alice_string_PT = Alice_string_PT.decode()
Alice_string_PT = json.loads(Alice_string_PT)

Bob_string_PT = Decryption(bytes.fromhex(to_KDC["Bob_string_cipher"]), kb)
Bob_string_PT = unpad(Bob_string_PT, DES.block_size)
Bob_string_PT = Bob_string_PT.decode()
Bob_string_PT = json.loads(Bob_string_PT)

if Alice_string_PT["R"] == temp_R and Bob_string_PT["R"] == temp_R:
    print("Authentication Successful")
    file = open("execution_order.txt", "a")
    file.write("Authentication Successful\n")
    file.write("\n")
    file.close()
else:
    print("Authentication Failed")

s.close()


s = get_socket(12346)
kab = os.urandom(8)
Bob_key_set = {
    "Rb": Bob_string_PT["Rb"],
    "kab": kab.hex()
}

Alice_key_set = {
    "Ra": Alice_string_PT["Ra"],
    "kab": kab.hex()
}

Alice_key_set = json.dumps(Alice_key_set)
Bob_key_set = json.dumps(Bob_key_set)

Alice_key_set_cipher = Encryption(Alice_key_set.encode(), ka)
Bob_key_set_cipher = Encryption(Bob_key_set.encode(), kb)

keyset_to_Bob = {
    "Alice_key_set_cipher": Alice_key_set_cipher.hex(),
    "Bob_key_set_cipher": Bob_key_set_cipher.hex(),
    "R": R
}

keyset_to_Bob = json.dumps(keyset_to_Bob)
# message = "From KDC to Bob"
s.send(keyset_to_Bob.encode())
s.close()
