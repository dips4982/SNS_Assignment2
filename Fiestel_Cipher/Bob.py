import socket
import json
from Crypto.Util.Padding import pad, unpad
# Bob

# def DES_Counter_Mode


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


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def f(part, key):
    roll_num = "52"
    roll_num_bin = to_bin(roll_num)
    pad_to = len(part)
    roll_num_bin = pad(roll_num_bin, pad_to)
    temp = byte_xor(part, key)
    return byte_xor(temp, roll_num_bin)


def to_ascii(decrypted_text):
    binary_int = int(decrypted_text, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    # Converting the array into ASCII text
    ascii_text = binary_array.decode()

    return ascii_text


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
    data = file.read()
    data_modif = json.loads(data)
    key1 = bytes.fromhex(data_modif["key1"])
    key2 = bytes.fromhex(data_modif["key2"])
    file.close()

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024)
        if not data:
            # if data is not received break
            break

        cipher_text = data
        ct_len = len(cipher_text)
        key1 = pad(key1, ct_len//2)
        key2 = pad(key2, ct_len//2)
        L3 = cipher_text[:ct_len//2]
        R3 = cipher_text[ct_len//2:]

        L4 = L3
        R4 = R3
        temp3 = f(L4, key2)
        L5 = byte_xor(temp3, R4)
        R5 = L4

        temp4 = f(L5, key1)
        L6 = byte_xor(temp4, R5)
        R6 = L5

        decrypt_cipher_text = L6 + R6
        print("Decrypted Cipher Text: " + str(decrypt_cipher_text))

        plain_text = ""
        size = len(decrypt_cipher_text)
        for x in range(0, size, 8):
            plain_text += to_ascii(decrypt_cipher_text[x:x+8])

        print("from connected user(after decryption): " + plain_text)
        # data = input(' -> ')
    # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
