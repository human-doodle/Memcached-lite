
from socket import *
import json
from collections import defaultdict
import threading, time

# Set the character encoding format
FORMAT = "utf-8"
# Define the server port
PORT = 9889
HOST = gethostname()    
IP = gethostbyname(HOST)  
ADDR =  (IP, PORT)


# function to check if integer
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        print('False')
        return False



def handle_client(connectionSocket, addr):

    # Define the JSON file
    file = "cache.json"

    try:
        while True:
                # take the command
                sentence = ""
                while True:
                    char = connectionSocket.recv(1).decode(FORMAT)
                    sentence += char
                    if sentence.endswith("\r\n"):
                        break
                
                # Create a defaultdict for key-value storage
                keyvalue = defaultdict()

                # Split the received command into parts
                command = [word.strip().lower() for word in sentence.split()]

                message = 'default message'

                # valid SET command
                if command[0] == 'set' and len(command) == 3 and is_integer(command[2]):
                        
                        # Try to open the JSON file for reading, if file doesn't exist, create an empty dictionary
                        try:
                            with open(file, 'r') as json_file:
                                d = json.load(json_file)
                        except FileNotFoundError:
                            d = {}
                        
                        # recieve the number of characters as recieved in the command
                        lent = int(command[2])
                        value = connectionSocket.recv(lent)

                        # Update the dictionary with the key-value pair
                        keyvalue[command[1]] = value.decode(FORMAT)
                        d.update(keyvalue)
                        
                        # Write the updated dictionary back to the JSON file
                        with open(file, 'w') as json_file:
                            json.dump(d, json_file, indent=4)

                        message =  'STORED \r\n'
                    
                # invalid set command
                elif command[0] == 'set' and (len(command) != 3 or not is_integer(command[2]) ):
                    message =  'NOT_STORED \r\n'
                    
                # get command
                elif command[0] == 'get': 
                    # valid get command
                    if len(command) == 2:
                        try:
                            # Try to open the JSON file for reading
                            with open(file, 'r') as json_file:
                                d = json.load(json_file)

                            # if key in file, return value
                            if command[1] in d:
                                value = d[command[1]]
                                
                                lent = len(value)

                                tosend = 'VALUE'+' '+ str(lent)+'\r\n'
                                connectionSocket.send(tosend.encode(FORMAT))
                                connectionSocket.send(value.encode(FORMAT))
                                message = 'END \r\n'

                            # key not in file, return invalid
                            else:
                                message = 'INVALID \r\n'
                                connectionSocket.send(message.encode(FORMAT))

                        except FileNotFoundError:
                            message = 'INVALID \r\n'
                            connectionSocket.send(message.encode(FORMAT))
                    else:
                        message = 'INVALID \r\n'

                # close connection for the pertiucular client
                elif command[0] == 'end':
                    break

                # invalid command
                else:
                    message = 'INVALID \r\n'

                # Send a response line back to the client
                connectionSocket.send(message.encode(FORMAT))
                #reset message
                message = ''

        print("[DISCONNECTED] Server Disconnected") 
        connectionSocket.close()

    except Exception as e:
        print(f"[ERROR] An error ococured: {e}")


def main():
    print("[STARTING] Server is starting")
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # pritn active connections 
        print(f"[ACTIVE CONNECTIONS] Active connections: {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()