import socket

# Define host and port
HOST = '127.0.0.1'
PORT = 3432

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((HOST, PORT))
    while True:
        # Get user input
        message = input("Enter message to send: ")
        # Send data to the server
        s.sendall(message.encode())
        # Receive response from the server
        data = s.recv(1024)
        print('Received from server:', data.decode())
