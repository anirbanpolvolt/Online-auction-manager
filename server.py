import socket
import threading
import time
import uuid
import sys

# Define host and port
HOST = '127.0.0.1'
PORT = 3430

# Flag to indicate whether the timer has finished
timer_finished = False

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

        while not timer_finished:
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
        if connection_counter == 0:
            highest_value = max(message_dict.values())
            print(highest_value)
            # timer_finished = True

def start_timer():
    global timer_finished
    print("Timer started. Waiting for 5 seconds...")
    time.sleep(100)
    print("100 seconds countdown completed. Exiting...")
    highest_value = max(message_dict.values())
    print(highest_value)
    timer_finished = True

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections
    server_socket.listen()
    print('Server listening on', HOST, PORT)

    # Start a new thread for the timer
    threading.Thread(target=start_timer).start()

    while not timer_finished:
        # Accept a connection
        conn, addr = server_socket.accept()
        # Handle the client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()
