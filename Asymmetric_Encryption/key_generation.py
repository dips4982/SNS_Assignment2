from Crypto.Util.number import *
from random import *
from hashlib import sha1


def generate_key():
    p = getPrime(10)
    q = getPrime(5)
    while (p - 1) % q != 0:
        p = getPrime(10)
        q = getPrime(5)

    e0 = randint(2, p - 1)
    e1 = pow(e0, (p - 1) // q) % p
    d = randint(1, p - 1)
    e2 = pow(e1, d) % p

    return p, q, d, e1, e2


def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


p, q, d, e1, e2 = generate_key()

key_params = ""
key_params += (str(p) + " " + str(q) + " " +
               str(d) + " " + str(e1) + " " + str(e2))
file = open('params.txt', 'w')
file.write(key_params)
file.close()
