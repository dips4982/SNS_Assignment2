from Crypto.Cipher import DES
from secrets import token_bytes
import os

key = os.urandom(8)
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
    binary_int = int(decrypted_text, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    # Converting the array into ASCII text
    ascii_text = binary_array.decode()

    return ascii_text


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


print(key)
input_text = input('Enter text to encrypt: ')
cipher_text = Encryption(input_text, counter)
print('Encrypted text: ', cipher_text)
plain_text = Decryption(cipher_text, counter)
print('Decrypted text: ', plain_text)
