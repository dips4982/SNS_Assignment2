from Crypto.Cipher import DES
from secrets import token_bytes
import os
from Crypto.Util.Padding import pad, unpad


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
    pad_to = len(key)
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


roll_num = "52"
roll_num_bin = to_bin(roll_num)
input_text = input('Enter text to encrypt: ')
input_text_bin = to_bin(input_text)
length = len(input_text_bin)//2
left = input_text_bin[:length]
right = input_text_bin[length:]
print(roll_num_bin)
print(left)
print(right)

key1 = os.urandom(length)
key2 = os.urandom(length)

# round 1

temp = f(right, key1)
R2 = byte_xor(temp, left)
L2 = right

# round2

temp2 = f(R2, key2)
R3 = byte_xor(temp2, L2)
L3 = R2

cipher_text = L3 + R3

print(cipher_text)


# Decryption

L4 = L3
R4 = R3

temp3 = f(L4, key2)
L5 = byte_xor(temp3, R4)
R5 = L4

temp4 = f(L5, key1)
L6 = byte_xor(temp4, R5)
R6 = L5

decrypt_cipher_text = L6 + R6
print(decrypt_cipher_text)

plain_text = ""
size = len(decrypt_cipher_text)
for x in range(0, size, 8):
    plain_text += to_ascii(decrypt_cipher_text[x:x+8])

print(plain_text)
