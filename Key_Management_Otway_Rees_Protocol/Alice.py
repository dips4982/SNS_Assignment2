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
Ra = data_modif["Ra"]
R = data_modif["R"]
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

s = get_socket(12346)
# message = "From Alice to Bob"
Alice_string = {
    "Alice": Alice_name,
    "Bob": Bob_name,
    "R": R,
    "Ra": Ra
}
Alice_string = json.dumps(Alice_string)
Alice_string_cipher = Encryption(Alice_string.encode(), ka)
to_Bob = {
    "Alice": Alice_name,
    "Bob": Bob_name,
    "R": R,
    "Alice_string_cipher": Alice_string_cipher.hex()
}
to_Bob = json.dumps(to_Bob)
s.send(to_Bob.encode())
s.close()

s = bind_socket(12345)
conn, addr = s.accept()
Alice_key_set_cipher = conn.recv(1024).decode()
# print("Alice_key_set_cipher: ", Alice_key_set_cipher)
# print(type(Alice_key_set_cipher))
Alice_key_set_PT = Decryption(bytes.fromhex(Alice_key_set_cipher), ka)
Alice_key_set_PT = unpad(Alice_key_set_PT, DES.block_size)
Alice_key_set_PT = Alice_key_set_PT.decode()
Alice_key_set_PT = json.loads(Alice_key_set_PT)
Alice_kab = bytes.fromhex(Alice_key_set_PT["kab"])
# print(data)
file = open("execution_order.txt", "a")
file.write("From Bob to Alice 4\n")
file.write("" + Alice_key_set_cipher + "\n")
file.write("\n")
file.close()
s.close()


s = get_socket(12346)
message = "This is a message sent from Alice to Bob"
cipher_message = Encryption(message.encode(), Alice_kab)
s.send(cipher_message)
s.close()
