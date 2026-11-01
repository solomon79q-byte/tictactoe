#Play game over LAN using UDP discovery and TCP for game communication. 
#The server listens for incoming connections and manages the game state, 
# while clients can connect to the server to play the game. 
# The server handles player turns, checks for wins or ties, 
# and updates the game board accordingly.


import socket

BROADCAST_PORT = 54321  # Port for UDP discovery


def upd_discovery_server(room_code):
    """
    Start a UDP discovery server that listens for incoming discovery requests.
    When a request is received, it responds with the servers IP address and port.
    """

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', BROADCAST_PORT)) 


    print(f"Creating a room with code: {room_code}")
    udp_socket.settimeout(30)  # Set a timeout for receiving data

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)  
            if data.decode() == f"DISCOVER:{room_code}":
                print(f"Found User at {addr}")

                response = f"{socket.gethostbyname(socket.gethostname())}:54321"  
                udp_socket.sendto(response.encode(), addr)
                return
        except socket.timeout:
            print("No discovery requests received in the last 30 seconds")
            break
    
    udp_socket.close()
    
def upd_discovery_client(room_code):
    """
    Start a UDP discovery client that broadcasts a discovery request to find the server.
    It listens for responses from servers and returns the first server found.
    """

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  

    discovery_message = f"DISCOVER:{room_code}".encode()
    print(f"Searching for Game Room with code: {room_code}")

    try:
        udp_socket.settimeout(5) 
        udp_socket.sendto(discovery_message, ('<broadcast>', BROADCAST_PORT)) 

        while True:
            try:
                data, addr = udp_socket.recvfrom(1024)  
                server_info = data.decode()
                print(f"Found Game Room at {server_info} from {addr}")
                return addr 
            except socket.timeout:
                print("No response received")
                return None
    finally:
        udp_socket.close() 


    