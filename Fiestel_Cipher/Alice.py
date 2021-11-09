import socket
import json
from Crypto.Util.Padding import pad, unpad
# Alice
# Two way channel for communication
# Alice -> Bob
# Bob -> Alice


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


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    file = open("params.txt", "r")
    data = file.read()
    data_modif = json.loads(data)
    key1 = bytes.fromhex(data_modif["key1"])
    key2 = bytes.fromhex(data_modif["key2"])
    file.close()

    input_text = input(" -> ")  # take input

    while input_text.lower().strip() != 'bye':
        input_text_bin = to_bin(input_text)
        length = len(input_text_bin)//2
        left = input_text_bin[:length]
        right = input_text_bin[length:]
        key1 = pad(key1, length)
        key2 = pad(key2, length)
        temp = f(right, key1)
        R2 = byte_xor(temp, left)
        L2 = right

        # round2

        temp2 = f(R2, key2)
        R3 = byte_xor(temp2, L2)
        L3 = R2

        cipher_text = L3 + R3
        client_socket.send(cipher_text)  # send input_text
        print("Cipher Text: " + str(cipher_text))

        input_text = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
