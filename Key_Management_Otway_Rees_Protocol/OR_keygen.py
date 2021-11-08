from Crypto.Cipher import DES
from secrets import token_bytes
from random import *
import os
import json


def Otway_Rees_keygen():
    ka = os.urandom(8)  # alice's key
    kb = os.urandom(8)  # bob's key

    Ra = randint(0, 10000)   # nonce from alice to KDC
    Rb = randint(0, 10000)   # nonce from bob to KDC
    R = randint(0, 10000)   # common nonce

    return ka, kb, Ra, Rb, R


# print("Alice's key: ", ka)
# print(type(ka))
# print("Bob's key: ", kb)
# print(type(kb))
# print("Alice's nonce: ", Ra)
# print(type(Ra))
# print("Bob's nonce: ", Rb)
# print(type(Rb))
# print("Common nonce: ", R)
# print(type(R))

ka, kb, Ra, Rb, R = Otway_Rees_keygen()


data = {
    "ka": ka.hex(),
    "kb": kb.hex(),
    "Ra": Ra,
    "Rb": Rb,
    "R": R
}

data_json = json.dumps(data)
file = open('OR_params.txt', 'w')
file.write(data_json)
file.close()

file = open("OR_params.txt", "r")
data = file.read()
data_modif = json.loads(data)
ka = bytes.fromhex(data_modif["ka"])
kb = bytes.fromhex(data_modif["kb"])
Ra = data_modif["Ra"]
Rb = data_modif["Rb"]
R = data_modif["R"]
file.close()
# print("Alice's key: ", ka)
# print(type(ka))
# print("Bob's key: ", kb)
# print(type(kb))
# print("Alice's nonce: ", Ra)
# print(type(Ra))
# print("Bob's nonce: ", Rb)
# print(type(Rb))
# print("Common nonce: ", R)
# print(type(R))
# print(ka==temp)
