from Crypto.Util.number import *
from random import *
from hashlib import sha1

'''
The Guillou-Quisquater protocol is an extension of the Fiat-Shamir protocol in which
fewer number of rounds can be used to prove the identity of the claimant. A trusted
third party chooses two large prime numbers p and q to calculate the
value of n = p × q. The trusted party also chooses an exponent, e, which is coprime with
φ, where φ = (p − 1)(q − 1). The values of n and e are announced to the public; the val-
ues of p and q are kept secret. The trusted party chooses two numbers for each entity, v
which is public and s which is secret. However, in this case, the relationship between v
and s is different: 
pow(s,e) × v = 1 mod n.

The three exchanges constitute a round;
Claimant sends witness x = pow(r,e)%n
Verifier sends challenge c, c is random number between 1 and e
Claimant sends response y = r*pow(s,c)%n

verification is repeated several times with
a random value of c (challenge) between 1 and e. The claimant must pass the test in
each round to be verified. If she fails a single round, the process is aborted and she is
not authenticated. Figure 14.16 shows one round.

if pow(y,e,n) * pow(v,c,n) == x Then Probable
Else Improbable


'''


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
print("p = ", p)
print("q = ", q)
print("n = ", n)
print("s = ", s)
print("e = ", e)
print("v = ", v)

r = randint(1, n)
x = pow(r, e, n)
c = randint(1, e)
y = (r * pow(s, c, n)) % n

if(pow(y, e, n)*pow(v, c, n) % n == x):
    print("Probable")
else:
    print("improbable")
