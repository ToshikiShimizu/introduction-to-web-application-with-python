import socket


class TCPServer:
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

            # get the response data to be sent to the client from the file
            with open("server_send.txt", "rb") as f:
                response = f.read()

            # send a response to the client
            client_socket.send(response)

            # the connection is terminated
            client_socket.close()

        finally:
            print("Stop the server")


if __name__ == '__main__':
    server = TCPServer()
    server.serve()
