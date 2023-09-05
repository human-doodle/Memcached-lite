import threading
import subprocess
import time

# Start a single client
def start_client(client_id):
    command = 'python client.py'
    
    # subprocess
    client_process = subprocess.Popen(
        command, 
        shell=True, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )

    # Send commands to the client's stdin
    def send_command(command):
        client_process.stdin.write(command + '\n')
        client_process.stdin.flush()

    # Sending commands throiugh stdin
    if client_id==1 or client_id == 8:
        command1 = 'set Rahul 7'
        command2 = 'Shivani'
        command3 = 'end'
        send_command(command1)
        send_command(command2)
        send_command(command3)
    elif client_id==5 or client_id == 9:
        command1 = 'get Rahul'
        command2 = 'end'
        send_command(command1)
        send_command(command2)
    else:
        command1 = 'set Rahul 4'
        command2 = 'Shivani'
        command3 = 'end'
        send_command(command1)
        send_command(command2)
        send_command(command3)

    # print the output from different client
    stdout, stderr = client_process.communicate()
    print(f"Client {client_id}:\n{stdout}\n")

# Start multiple clients concurrently
def start_multiple_clients(num_clients):
    threads = []

    # starting each client in a separate thread
    for i in range(1, num_clients + 1):
        thread = threading.Thread(target=start_client, args=(i,))
        threads.append(thread)
        thread.start()

    # Waiting for all threads to finish
    for thread in threads:
        thread.join()

# test cases with 10, 20, 30, 40
start = time.time()
start_multiple_clients(20)
end = time.time()
print(end-start)
