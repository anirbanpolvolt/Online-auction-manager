import socket
import threading
import uuid

# Define host and port
HOST = '127.0.0.1'
PORT = 3432

# Create a dictionary to store messages
message_dict = {}
# Counter to keep track of the number of connections
connection_counter = 0
# Lock to ensure thread safety when updating the counter
counter_lock = threading.Lock()

def handle_client(conn, addr):
    global connection_counter

    with conn:
        client_id = uuid.uuid4().hex  # Generate a unique client ID
        print('Connected by', addr, 'with client ID:', client_id)
        
        # Increment connection counter when a new connection is established
        with counter_lock:
            connection_counter += 1
            print('Number of connections:', connection_counter)
            if coune

        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                break
            # Deserialize the received data
            message = data.decode()
            # Add message to the dictionary with the client ID as the key
            message_dict[client_id] = message
            print('Received from', client_id + ':', message)
            # Send a response back to the client
            conn.sendall(b'Message received by the server')

        # Decrement connection counter when a connection is closed
        with counter_lock:
            connection_counter -= 1
            print('Number of connections:', connection_counter)
            threading.Timer(10, server_socket.close).start()

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections
    server_socket.listen()
    print('Server listening on', HOST, PORT)

    while True:
        # Accept a connection
        conn, addr = server_socket.accept()
        # Start a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()
