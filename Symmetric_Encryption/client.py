import socket
from Crypto.Cipher import DES
from secrets import token_bytes
import os

key = b'\x8e\xc8U!\xa0\x14o\xc1'
counter = b'00101100'
counter2 = b'00101100'


def to_bin(inp):
    temp = ""
    res = ""
    # inp = inp.encode('ascii')
    for i in inp:
        temp = "{0:b}".format(int(ord(i)))
        while len(temp) < 8:
            temp = "0" + temp
        res += temp

    return res.encode('ascii')


def encrypt(msg):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(msg)
    return ciphertext


def decrypt(ciphertext):
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)

    try:
        return plaintext
    except:
        return False


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def increment_binary_string(s):
    temp = '{:04b}'.format(1 + int(s, 2))
    while len(temp) < 8:
        temp = "0" + temp

    return temp.encode('ascii')


def to_ascii(decrypted_text):
    try:
        binary_int = int(decrypted_text, 2)
        # Getting the byte number
        byte_number = binary_int.bit_length() + 7 // 8
        # Getting an array of bytes
        binary_array = binary_int.to_bytes(byte_number, "big")
        # Converting the array into ASCII text
        ascii_text = binary_array.decode()

        return ascii_text

    except Exception as e:
        print(e)
        return ""


def Encryption(plaintext, counter):
    encrypted_counter = encrypt(counter)
    input_text_bin = to_bin(plaintext)
    size = len(input_text_bin)
    cipher_text = b''
    for x in range(0, size, 8):
        encrypted_text = byte_xor(encrypted_counter, input_text_bin[x:x+8])
        cipher_text += encrypted_text
        counter = increment_binary_string(counter)
        encrypted_counter = encrypt(counter)

    return cipher_text


def Decryption(ciphertext, counter):
    encrypted_counter = encrypt(counter)
    size = len(ciphertext)
    plaintext = ""
    for x in range(0, size, 8):
        decrypted_text = byte_xor(encrypted_counter, ciphertext[x:x+8])
        plaintext += to_ascii(decrypted_text)
        counter = increment_binary_string(counter)
        encrypted_counter = encrypt(counter)

    return plaintext
# Alice
# Two way channel for communication
# Alice -> Bob
# Bob -> Alice


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        cipher_text = Encryption(message, counter)
        client_socket.send(cipher_text)  # send message
        # client_socket.send(test)  # send message
        # client_socket.send(message.encode())
        data = client_socket.recv(1024)  # receive response
        print('Cipher Text Received :')
        print(data)
        plain_text = Decryption(data, counter)
        print('Received from server (after decryption): ' +
              plain_text)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
