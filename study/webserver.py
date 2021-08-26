import socket
from datetime import datetime

class WebServer:
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
            print("The connection with the client is complete. remote_address: {}".format(address))

            # get the data sent from the client
            request = client_socket.recv(4096)

            # write the data sent from the client to a file
            with open("server_recv.txt", "wb") as f:
                f.write(request)

            # generate response body
            response_body = "<html><body><h1>It works!</h1></body></html>"

            # generate response line
            response_line = "HTTP/1.1 200 OK\r\n"

            # generate response header
            response_header = ""
            response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            response_header += "Host: HenaServer/0.1\r\n"
            response_header += f"Content-Length: {len(response_body.encode())}\r\n"
            response_header += "Connection: Close\r\n"
            response_header += "Content-Type: text/html\r\n"

            # after attaching the header and body with a blank line, convert it to bytes and generate the entire response
            response = (response_line + response_header + "\r\n" + response_body).encode()

            # send a response to the client
            client_socket.send(response)

            # the connection is terminated
            client_socket.close()

        finally:
            print("Stop the server")


if __name__ == '__main__':
    server = WebServer()
    server.serve()
