import os
import socket
from datetime import datetime


class WebServer:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    def serve(self):
        print("Start the server.")
        try:
            # create socket
            server_socket = socket.socket()
            server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # assign socket to localhost port 8080
            server_socket.bind(("localhost", 8080))
            server_socket.listen(10)

            # wait for a connection from the outside and estabish a connection if there is a connection
            print("Wait for a connection")
            (client_socket, address) = server_socket.accept()
            print("The connection with the client is complete. remote_address: {}".format(
                address))

            # get the data sent from the client
            request = client_socket.recv(4096)

            # write the data sent from the client to a file
            with open("server_recv.txt", "wb") as f:
                f.write(request)

            # parse the entire request
            request_line, remain = request.split(b"\r\n", maxsplit=1)
            request_header, request_body = remain.split(
                b"\r\n\r\n", maxsplit=1)

            # parse the request line
            method, path, http_version = request_line.decode().split(" ")

            # delete / at the beginning of path and make it a relative path
            relative_path = path.lstrip("/")

            # get the path of the file
            static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

            # debug
            print(path)
            print(relative_path)
            print(static_file_path)

            # generate a response body from a file
            try:
                with open(static_file_path, "rb") as f:
                    response_body = f.read()
            except OSError:
                # returns a 404 if the file is not found
                response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                response_line = "HTTP/1.1 404 Not Found\r\n"

            # generate response line
            response_line = "HTTP/1.1 200 OK\r\n"

            # generate response header
            response_header = ""
            response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            response_header += "Host: HenaServer/0.1\r\n"
            response_header += f"Content-Length: {len(response_body)}\r\n"
            response_header += "Connection: Close\r\n"
            response_header += "Content-Type: text/html\r\n"

            # after attaching the header and body with a blank line, convert it to bytes and generate the entire response
            response = (response_line + response_header +
                        "\r\n").encode() + response_body

            # send a response to the client
            client_socket.send(response)

            # the connection is terminated
            client_socket.close()

        finally:
            print("Stop the server")


if __name__ == '__main__':
    server = WebServer()
    server.serve()
