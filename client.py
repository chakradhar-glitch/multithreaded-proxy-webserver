import socket

IP_ADDRESS = "127.0.0.1"
PORT = 12345
ADDR = (IP_ADDRESS, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = '!Disconnect'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)

    send_len += b' ' * (HEADER - len(send_len))

    # send len
    client.send(send_len)

    # send msg
    client.send(message)

    print(client.recv(1024).decode(FORMAT))


input()
send('Hello Chakri!')
input()
send("Hello ALl")
input()
send('!Disconnect')


