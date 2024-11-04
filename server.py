import socket
import threading
import logging
import gzip
from urllib.parse import urlparse
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("proxy_server.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)


def proxy_thread(client_socket, addr):
    try:
        logging.info(f"[NEW CONNECTION] {addr} connected")
        request = client_socket.recv(4096).decode(FORMAT)

        # extract target url from the request
        split_request = request.split('\n')
        first_line = split_request[0]
        # logging.info(f'received request header: {first_line}')
        # logging.info(f"received host: {split_request[1]}")

        url = first_line.split(' ')[1][1:]
        port = -1
        if url.startswith('http:'):
            port = 80

        else:
            port = 443

        url_len = len(url)
        colon = url.find('://')
        host = url[colon+3:url_len-1]

        if port == 443:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                logging.info(f'Establishing connection to {host} {port}')
                server_socket.connect((host, port))
                # client_socket.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')

                # Forward the data between client and server
                while True:
                    # data = client_socket.recv(4096)
                    # if not data:
                    #     break
                    logging.info(f'Forwarding request...')
                    server_socket.sendall(request.encode())
                    response = server_socket.recv(4096)
                    logging.info('Response received...')
                    logging.info(f"Response is: {response.decode()}")
                    client_socket.sendall(response)
                    logging.info('Sending back response...')

        else:

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.info(f'Establishing connection to {host}:{port}')
            server_socket.connect((url, port))

            server_socket.sendall(request.encode())

            # get the response from target server
            while True:
                response = server_socket.recv(4096)
                if not response:
                    break
                client_socket.send(response)
                logging.info(
                    f"Response sent to client: {client_socket.getpeername()}")  # Get the address of the connected client

    except Exception as e:
        logging.error(f"Error processing the request: {str(e)}", stack_info=True)

    finally:
        client_socket.close()


def main():
    try:
        server.listen(1)
        logging.info(f'LISTENING on {IP_ADDRESS}')

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=proxy_thread, args=(conn, addr), daemon=True)
            thread.start()

            logging.info(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

    except Exception as e:
        logging.error(f'Error in main: {str(e)}')


main()
