import socket
import threading

# reqs
IP_ADDRESS = "127.0.0.1"
PORT = 12345
ADDR = (IP_ADDRESS, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = '!Disconnect'

# create a tcp socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket
server.bind(ADDR)


def handle_client(conn, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MSG:
                    connected = False

                print(f'[{addr} {msg}]')
                conn.send('Msg received'.encode(FORMAT))
        conn.close()
    except Exception as e:
        print(str(e))
        raise e


def main():
    try:
        server.listen()
        print(f'LISTENING on {IP_ADDRESS}')

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

            print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

    except Exception as e:
        print(str(e))
        raise e


main()
