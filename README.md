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

## Symmetric Encryption

DES Algorithm with Counter Mode has been used
Files :
Alice.py : contains code for Encryption using DES in counter mode
Bob.py   : contains code for Decryption

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

Digital Signature Standard Algorithm has been used
Files : 
DSS_key_generation.py : Run this file to generate required set of parameters and keys
params.txt            : Stores the output of key generation
Verifier_Bob.py       : conatins code for verification of signature
Signer_Alice.py       : contains code for signing and sending the data

To execute : 

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



