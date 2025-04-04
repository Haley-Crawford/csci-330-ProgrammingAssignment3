import re
import socket
import os.path as path
import sys

IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str, address: (str, int)):
    # get the file size in bytes
    file_size = get_file_size(file_name)

    # convert file_size to an 8-byte byte string using big endian
    file_size = file_size.to_bytes(8, byteorder='big')

    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(address)
        input("Hit return to continue...")
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        client_socket.send(file_size + file_name.encode())
        print(f'Sending {file_size + file_name.encode()}')
        data = client_socket.recv(BUFFER_SIZE)
        if data != b'go ahead':
            raise OSError('Bad server response - was not go ahead')
        # open the file to be transferred
        with open(file_name, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            is_done = False
            while not is_done:
                chunk = file.read(BUFFER_SIZE)
                if len(chunk) > 0:
                    print(f'sending chunk of length {len(chunk)}')
                    client_socket.send(chunk)
                else:
                    is_done = True
    except OSError as e:
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename> [IP address] [Port]')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) > 2:
        IP = sys.argv[2]
    try:
        # if port is provided on cmdline, then use it
        if len(sys.argv) > 3:
            PORT = int(sys.argv[3])
    except ValueError as ve:
        print(ve)

    ret_value = send_file(file_name, (IP, PORT))
    sys.exit(ret_value)
