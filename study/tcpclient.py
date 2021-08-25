import socket


class TCPClient:
    def request(self):
        print("Start the client")
        try:
            # create socket
            client_socket = socket.socket()
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # connect to server
            print("Connect with the server")
            client_socket.connect(("127.0.0.1", 80))
            print("Completed connection with server")

            # get the request to send to the server from the file
            with open("client_send.txt", "rb") as f:
                request = f.read()

            # send a request to the server
            client_socket.send(request)

            # wait for a response from the server and get it
            response = client_socket.recv(4096)

            # write the contents of the response to a file
            with open("client_recv.txt", "wb") as f:
                f.write(response)

            # end connection
            client_socket.close()

        finally:
            print("Stop the client")


if __name__ == '__main__':
    client = TCPClient()
    client.request()
