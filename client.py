from socket import *
from collections import *

# SET client configurations
HOST = gethostname() 
IP = gethostbyname(HOST) 
PORT = 9889
ADDR =  (HOST,PORT)
FORMAT = "utf-8"


def main():
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM) 
        clientSocket.connect(ADDR) 
        while 1:
                sentence = input("") 
                
                command = sentence.split(' ')
                tosend = sentence+'\r\n'
                # send to server
                clientSocket.send(tosend.encode(FORMAT))


                # handle set
                if command[0]=='set' and len(command)==3:
                    
                    if  command[2].isnumeric():
                        value = input('') 
                        clientSocket.send(value[:int(command[2])].encode(FORMAT))
                    
                    
                # handle get 
                elif command[0]=='get' and len(command)==2:
                    data = ""
                    while True:
                        char = clientSocket.recv(1).decode(FORMAT)
                        data += char
                        if data.endswith("\r\n"):
                            break
                    if data.strip()!='INVALID':
                        value = clientSocket.recv(int(data.split(" ")[1]))
                        print(value.decode(FORMAT))

                # handle end
                elif command[0] == 'end':
                    tosend = command[0]+'\r\n'
                    clientSocket.send(tosend.encode(FORMAT))
                    break


                # recieve message from server
                message = ""
                while True:
                            char = clientSocket.recv(1).decode(FORMAT)
                            message += char
                            if message.endswith("\r\n"):
                                break

                # print to stdout
                print(message) 

        # close connection
        clientSocket.close()    
            
    except Exception as e:
                print(e)

if __name__ == "__main__":
    main()