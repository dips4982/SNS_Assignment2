from Crypto.Util.number import *
from random import *
from hashlib import sha1

# choose p in multiple of 64 bits - Ideally
# for computation purposes we take smaller value of bits



# generate set of alice's public key set e1,,e2,p,q and private key(d)
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


def signing(message, p, q, d, e1, e2):
    # r is the random secret
    r = randint(2, p - 1)
    r_inverse = mod_inverse(r, q)
    hashed_message = sha1(message.encode("UTF-8")).hexdigest()
    hash_val = int(hashed_message, 16)
    s1 = (pow(e1, r) % p) % q
    s2 = ((hash_val+d*s1)*r_inverse) % q

    return r, s1, s2


def verifying(message, p, q, e1, e2, s1, s2):
    hashed_message = sha1(message.encode("UTF-8")).hexdigest()
    hash_val = int(hashed_message, 16)
    s2_inverse = mod_inverse(s2, q)

    w = mod_inverse(s1, q)
    # u1 = (hash_val * w) % q
    # u2 = (r * w) % q
    v = ((pow(e1, (hash_val*s2_inverse) % q) *
         pow(e2, (s1*s2_inverse) % q)) % p) % q
    if v == s1:
        print("Valid Signature")
        return True
    else:
        print("Invalid Signature")
        return False


p, q, d, e1, e2 = generate_key()
r, s1, s2 = signing("hello bhai kaisa hai!", p, q, d, e1, e2)


print("p: ", p)
print("q: ", q)
print("e1: ", e1)
print("e2: ", e2)
print("d: ", d)
print("r: ", r)
print("s1: ", s1)
print("s2: ", s2)

print(verifying("hello bhai kaisa hai", p, q, e1, e2, s1, s2))
