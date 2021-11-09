# Systems And Network Security

This repository contains Python implementation for DES in counter mode, Digital Signature Standard, Entity Authentication using Guillou Quisquarter protocol, Key Management using Otway Rees Protocol. Socket Programming has been used to demonstrate communication across different entities.

## Installation

To setup project in your local

```bash
git clone https://github.com/dips4982/SNS_Assignment2.git 
```

Install Pycryptodome package

```bash
pip install pycryptodome
```
## Two Round Fiestal Cipher

Files :\
keygen.py  : Genertes keys 1 and 2 require for two rounds\
params.txt : Stores the output of key_generation\
Alice.py   : code for client that sends encrypted text\
Bob.py     : code for server that receives encrypted text and decrypts it\

To execute :\ 

To generate keys 

```bash
python3 DSS_keygen.py
```

First Run Bob.py acts as server

```bash
python3 Bob.py
```
Then Run Alice.py in seperate terminal

```bash
python3 Alice.py
```

## Symmetric Encryption

DES Algorithm with Counter Mode has been used\
Files :\
Alice.py : contains code for Encryption using DES in counter mode\
Bob.py   : contains code for Decryption\

To execute : 

Run Bob.py who acts as server

```bash
python3 Bob.py
```

Run Alice.py in seperate terminal

```bash
python3 Alice.py
```

## Asymmetric Encryption

Digital Signature Standard Algorithm has been used\

Files :\
DSS_key_generation.py : Run this file to generate required set of parameters and keys\
params.txt            : Stores the output of key generation\
Verifier_Bob.py       : conatins code for verification of signature\
Signer_Alice.py       : contains code for signing and sending the data\

To execute :\ 

To generate keys 

```bash
python3 DSS_key_generation.py
```

First run Verifier_Bob.py since it will act as a server

```bash
python3 Verifier_Bob.py
```

Then run Signer_Alice.py in a seperate terminal

```bash
python3 Signer_Alice.py
```

## Entity Authentication

Entity Authentication is implemented using Guillou-Quisquater protocol\
The three exchanges constitute a round;\
Claimant sends witness x = pow(r,e)%n\
Verifier sends challenge c, c is random number between 1 and e\
Claimant sends response y = r*pow(s,c)%n\

Files :\
GQ_key_generation.py : Generates keys and parameters required for Entity Authentication\
params.txt           : Saves output of above key generation\
Claimant_Alice.py    : code for claimant\
Verifier_Bob.py      : code for verifier\

To execute :

Generate keys and params :

```bash
python3 GQ_key_generation.py
```

First Run Verifier_Bob.py which acts as server

```bash
python3 Verifier_Bob.py
```

Then Run Claimant_Alice.py which is the client

```bash
python3 Claimant_Alice.py
```
## Key Management (Session Key Distribution Protocol)

Otway Rees Protocol has been implemented\
Three Entities : Alice, Bob and KDC(key distribution center)\

Files :\
OR_keygen.py        : Generates keys and parameters\
OR_params.txt       : stores output of above file\
Alice.py            : code for entity representing Alice\
Bob.py              : code for entity representing Bob\
KDC.py              : code for Key Distribution Center\
execution.order.txt : stores the log of execution flow of the complete program.\

To Execute :\

Generate keys and params :

```bash
python3 OR_keygen.py
```

First Run Bob.py

```bash
python3 Bob.py
```

Then Run KDC.py in seperate terminal

```bash
python3 KDC.py
```

Then Run Alice.py in seperate terminal
 
```bash
python3 Alice.py
```
After successfull execution, the log will be saved in execution_order.txt



