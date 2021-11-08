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
Ra = data_modif["Ra"]
Rb = data_modif["Rb"]
R = data_modif["R"]

temp_ka = ka
temp_kb = kb
temp_Ra = Ra
temp_Rb = Rb
temp_R = R


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


Alice_string = {
    "Alice": Alice_name,
    "Bob": Bob_name,
    "R": R,
    "Ra": Ra
}

Alice_string = json.dumps(Alice_string)
Alice_string_cipher = Encryption(Alice_string.encode(), ka)
# Alice_string_plain = Decryption(Alice_string_cipher, ka).decode()
# print(Alice_string_cipher)
# print(Alice_string_plain)

# Alice sends Alice,Bob,R and (Alice,Bob,R,Ra) encrypted with ka to Bob
to_Bob = {
    "Alice": Alice_name,
    "Bob": Bob_name,
    "R": R,
    "Alice_string_cipher": Alice_string_cipher
}

# to KDC

# print(to_Bob["Alice_string_cipher"])
Alice = to_Bob["Alice"]
Bob = to_Bob["Bob"]
R = to_Bob["R"]
Alice_string_cipher = to_Bob["Alice_string_cipher"]

Bob_string = {
    "Alice": Alice,
    "Bob": Bob,
    "R": R,
    "Rb": Rb
}
Bob_string = json.dumps(Bob_string)
Bob_string_cipher = Encryption(Bob_string.encode(), kb)

to_KDC = {
    "Alice_string_cipher": Alice_string_cipher,  # encrypted with ka
    "Bob_string_cipher": Bob_string_cipher       # encrypted with kb
}

# Decryption at KDC

Alice_string_PT = Decryption(to_KDC["Alice_string_cipher"], ka)
Alice_string_PT = unpad(Alice_string_PT, DES.block_size)
Alice_string_PT = Alice_string_PT.decode()
Alice_string_PT = json.loads(Alice_string_PT)

Bob_string_PT = Decryption(to_KDC["Bob_string_cipher"], kb)
Bob_string_PT = unpad(Bob_string_PT, DES.block_size)
Bob_string_PT = Bob_string_PT.decode()
Bob_string_PT = json.loads(Bob_string_PT)

if Alice_string_PT["R"] == temp_R and Bob_string_PT["R"] == temp_R:
    print("Authentication Successful")
else:
    print("Authentication Failed")

kab = os.urandom(8)  # Session key for Alice and Bob

Bob_key_set = {
    "Rb": Bob_string_PT["Rb"],
    "kab": kab.hex()
}

Alice_key_set = {
    "Ra": Alice_string_PT["Ra"],
    "kab": kab.hex()
}

# send keyset to Bob

Alice_key_set = json.dumps(Alice_key_set)
Bob_key_set = json.dumps(Bob_key_set)

Alice_key_set_cipher = Encryption(Alice_key_set.encode(), ka)
Bob_key_set_cipher = Encryption(Bob_key_set.encode(), kb)

keyset_to_Bob = {
    "Alice_key_set_cipher": Alice_key_set_cipher,
    "Bob_key_set_cipher": Bob_key_set_cipher,
    "R": R
}

# received at Bob
Bob_key_set_PT = Decryption(keyset_to_Bob["Bob_key_set_cipher"], kb)
Bob_key_set_PT = unpad(Bob_key_set_PT, DES.block_size)
Bob_key_set_PT = Bob_key_set_PT.decode()
Bob_key_set_PT = json.loads(Bob_key_set_PT)
Bob_kab = bytes.fromhex(Bob_key_set_PT["kab"])
# here bob has got the session key

# send keyset to Alice
Alice_key_set_PT = Decryption(keyset_to_Bob["Alice_key_set_cipher"], ka)
Alice_key_set_PT = unpad(Alice_key_set_PT, DES.block_size)
Alice_key_set_PT = Alice_key_set_PT.decode()
Alice_key_set_PT = json.loads(Alice_key_set_PT)
Alice_kab = bytes.fromhex(Alice_key_set_PT["kab"])
# here Alice has got the session key

print(temp_ka)
print(temp_kb)
print(Bob_kab)
print(Alice_kab)

message = "Hello Bob"
cipher_message = Encryption(message.encode(), Alice_kab)
plain_message = Decryption(cipher_message, Bob_kab)
plain_message = unpad(plain_message, DES.block_size)
plain_message = plain_message.decode()
print(plain_message)
