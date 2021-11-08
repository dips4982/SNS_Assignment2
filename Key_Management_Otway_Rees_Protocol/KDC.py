import socket

def get_socket(port):
    s = socket.socket()
    s.connect(("127.0.0.1", port))
    return s


def bind_socket(port):
    s = socket.socket()
    s.bind(("", port))
    s.listen(5)
    return s

# port alice = 12345
# port bob = 12346
# port kdc = 12347

s = bind_socket(12347)
conn, addr = s.accept()
data  = conn.recv(1024).decode()
print(data)
file = open("execution_order.txt", "a")
file.write("" + data + "\n")
file.close()
s.close()

s = get_socket(12346)
message = "From KDC to Bob"
s.send(message.encode())
s.close()



