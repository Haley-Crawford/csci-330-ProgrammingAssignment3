import random
import socket
import os
import sys

IP = '127.0.0.1'  # default IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8],byteorder='big')


def upload_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data
    # Add a random number to the filename ending
    file_name += '.temp'+str(random.randint(1001,9999))
    # please do not change the above line!
    with open(file_name, 'wb') as file:
        retrieved_size = 0
        try:
            while retrieved_size < file_size:
                # TODO: section 1 step 6a
                # TODO: section 1 stop 6b
                # TODO: section 1 stop 6c
        except OSError as oe:
            print(oe)
            os.remove(file_name)

def service_client_connection(conn_socket: socket):
    try:
        # TODO: section 3 step 2
        # expecting an 8-byte byte string for file size followed by file name
        # TODO: section 3 step 3
        print(f'Received: {file_name} with size = {file_size}')
        # TODO: section 3 step 4
        upload_file(conn_socket, file_name, file_size)
    except Exception as e:
        print(e)
    finally:
        conn_socket.close()
def start_server(ip, port):
    # create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port)) # section 3 and 4 step 1
    server_socket.listen(5) # section 4 step 2
    print(f'Server ready and listening on {ip}:{port}')
    try:
        while True: # section 4 step 6
            (conn_socket, addr) = server_socket.accept() # section 4 step 3
            # TODO: section 4 step 4
            # TODO: section 4 step 5
    except KeyboardInterrupt as ki:
        pass
    finally:
        server_socket.close()


if __name__ == "__main__":
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    try:
        # if port is provided on cmdline, then use it
        if len(sys.argv) > 2:
            PORT = int(sys.argv[2])
    except ValueError as ve:
        print(ve)

    start_server(IP, PORT)