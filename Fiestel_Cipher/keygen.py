import os
import json

key1 = os.urandom(8)
key2 = os.urandom(8)

data = {
    "key1": key1.hex(),
    "key2": key2.hex()
}

data_json = json.dumps(data)
file = open('params.txt', 'w')
file.write(data_json)
file.close()
