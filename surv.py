#!/usr/bin/python

import mimetypes
import socket

server_socket = socket.create_server(("", 8080))

def request_loop():
    connection_socket, address = server_socket.accept()

    lines = connection_socket.recv(1024).decode().splitlines()
    if len(lines) == 0:
        return
    
    first_line_parts = lines[0].split(' ')

    verb = first_line_parts[0]
    path = first_line_parts[1]
    mimetype = mimetypes.guess_type(path)[0]

    if verb == 'GET':
        print(address[0], "\trequested\t", path, end='\t')

        try:
            with open("./" + path) as file:
                file_contents = file.read().encode()
                connection_socket.send(b'HTTP/1.1 200 OK\n')
                connection_socket.send(b'Content-Type: %s \n' % mimetype.encode())
                connection_socket.send(b'Content-Length: %i \n' % len(file_contents))
                connection_socket.send(b'HttpOnly\n\n')
                connection_socket.sendall(file_contents)
                print('200')
        except (FileNotFoundError, IsADirectoryError) as exception:
            connection_socket.send(b'HTTP/1.1 404 Not Found\n')
            connection_socket.send(b"prolly 404\n")
            print('404')
        finally:
            connection_socket.close()

while True:
    try:
        request_loop()
    except KeyboardInterrupt:
        exit()
