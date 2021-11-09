from Crypto.Util.number import *
from random import *
from hashlib import sha1
import json


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


def Guillou_Quisquater():
    p = getPrime(10)
    q = getPrime(5)
    n = p*q
    e = 3
    while GCD(e, (p-1)*(q-1)) != 1:
        e = getPrime(5)

    s = randint(1, (p-1)*(q-1))
    v = mod_inverse(pow(s, e), n)
    return (p, q, n, s, e, v)


p, q, n, s, e, v = Guillou_Quisquater()

data = {
    "p": p,
    "q": q,
    "n": n,
    "s": s,
    "e": e,
    "v": v
}

data_json = json.dumps(data)
file = open('params.txt', 'w')
file.write(data_json)
file.close()
