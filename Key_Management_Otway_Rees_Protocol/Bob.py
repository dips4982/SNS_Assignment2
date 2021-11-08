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
Rb = data_modif["Rb"]
file.close()

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
s = bind_socket(12346)
conn, addr = s.accept()
to_Bob = conn.recv(1024).decode()
file = open("execution_order.txt", "a")
file.write("From Alice to Bob 1\n")
file.write("" + to_Bob + "\n")
file.write("\n")
file.close()
# print(data)
to_Bob = json.loads(to_Bob)
Alice = to_Bob["Alice"]
Bob = to_Bob["Bob"]
R = to_Bob["R"]
Alice_string_cipher = bytes.fromhex(to_Bob["Alice_string_cipher"])
s.close()


s = get_socket(12347)
Bob_string = {
    "Alice": Alice,
    "Bob": Bob,
    "R": R,
    "Rb": Rb
}
Bob_string = json.dumps(Bob_string)
Bob_string_cipher = Encryption(Bob_string.encode(), kb)
to_KDC = {
    "Alice_string_cipher": Alice_string_cipher.hex(),  # encrypted with ka
    "Bob_string_cipher": Bob_string_cipher.hex()       # encrypted with kb
}
to_KDC = json.dumps(to_KDC)
# message = "From Bob to KDC"
s.send(to_KDC.encode())
s.close()

s = bind_socket(12346)
conn, addr = s.accept()
# receive from KDC
keyset_to_Bob = conn.recv(1024).decode()
# print(data)
file = open("execution_order.txt", "a")
file.write("From KDC to Bob 3\n")
file.write("" + keyset_to_Bob + "\n")
file.write("\n")
file.close()

keyset_to_Bob = json.loads(keyset_to_Bob)
Bob_key_set_PT = Decryption(bytes.fromhex(
    keyset_to_Bob["Bob_key_set_cipher"]), kb)
Bob_key_set_PT = unpad(Bob_key_set_PT, DES.block_size)
Bob_key_set_PT = Bob_key_set_PT.decode()
Bob_key_set_PT = json.loads(Bob_key_set_PT)
Bob_kab = bytes.fromhex(Bob_key_set_PT["kab"])

s.close()


s = get_socket(12345)
Alice_key_set_cipher = keyset_to_Bob["Alice_key_set_cipher"]
# message = "From Bob to Alice"
s.send(Alice_key_set_cipher.encode())
s.close()

s = bind_socket(12346)
conn, addr = s.accept()
cipher_message = conn.recv(1024)
plain_message = Decryption(cipher_message, Bob_kab)
plain_message = unpad(plain_message, DES.block_size)
plain_message = plain_message.decode()
print(plain_message)
file = open("execution_order.txt", "a")
file.write("Alice to Bob 5\n")
file.write("" + cipher_message.hex() + "\n")
file.write("\n")
file.write("" + plain_message + "\n")
file.close()
s.close()
