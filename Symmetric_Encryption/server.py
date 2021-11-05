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

    except ValueError:
        return ""

    except TypeError:
        pass


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
    decrypted_counter = encrypt(counter)
    size = len(ciphertext)
    plaintext = ""
    for x in range(0, size, 8):
        decrypted_text = byte_xor(decrypted_counter, ciphertext[x:x+8])
        plaintext += to_ascii(decrypted_text)
        counter = increment_binary_string(counter)
        decrypted_counter = encrypt(counter)

    return plaintext
# Bob

# def DES_Counter_Mode


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
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024)
        print(data)
        plain_text = Decryption(data, counter)
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(plain_text))
        data = input(' -> ')
        ciphertext = Encryption(data, counter)
        conn.send(ciphertext)  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
