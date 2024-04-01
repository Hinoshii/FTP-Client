import socket
from getpass import getpass
import random
import os

connected = False

while True:
    line = input('ftp> ').strip()
    args = line.split()
    if args != []:
        commands = args[0]
        commands = commands.lower()
    else :
        commands = ""

    if commands == 'quit' or commands == 'bye':
        if connected :
            clientSocket.send(str('QUIT\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
            clientSocket.close()
            connected = False
        print()
        break

    elif commands == 'ascii':
        if connected :
            clientSocket.send(str('TYPE A\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'binary':
        if connected :
            clientSocket.send(str('TYPE I\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'cd':
        if connected :
            clientSocket.send(str('CWD '+ args[1] + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'delete':
        if connected :
            clientSocket.send(str('DELE ' + args[1] + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'get':
        if connected:
            ftp_server_ip_v4 = clientSocket.getsockname()[0]
            ftp_server_ip_v4_formatted = ",".join(ftp_server_ip_v4.split('.'))
            port_first_half = random.randint(127,255)
            port_second_half = random.randint(0,255)
            port_formatted = str(port_first_half) + ',' + str(port_second_half)
            port = port_first_half*256 + port_second_half

            clientSocket.send(str('PORT '+ ftp_server_ip_v4_formatted + ',' + port_formatted + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')

            if resp.decode().startswith("200"):
                clientSocket.send(str('RETR ' + args[1] + '\r\n').encode('utf-8'))
                newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                newsocket.bind((ftp_server_ip_v4,port))
                newsocket.listen(10)
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')

                if len(args) == 3:
                    local_path = os.path.join(os.getcwd(), args[2])
                else:
                    local_path = os.path.join(os.getcwd(), args[1])

                if resp.decode().startswith("1"):
                    connectionSocket, addr = newsocket.accept()

                    with open(local_path, 'w') as file:
                        file.write('')

                    data = b""
                    while True:
                        data_recv = connectionSocket.recv(1024)
                        data += data_recv
                        if not data_recv:
                            break
                    
                    with open(local_path, 'wb') as file:
                        file.write(data)

                    size_data = len(data)
                
                    connectionSocket.close()
                newsocket.close()
                
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
                print(f'ftp: {size_data} bytes received in 0.00Seconds veryFast bytes/sec.')
        else :
            print('Not connected.')

    elif commands == 'ls':
        if connected:
            ftp_server_ip_v4 = clientSocket.getsockname()[0]
            ftp_server_ip_v4_formatted = ",".join(ftp_server_ip_v4.split('.'))
            port_first_half = random.randint(127,255)
            port_second_half = random.randint(0,255)
            port_formatted = str(port_first_half) + ',' + str(port_second_half)
            port = port_first_half*256 + port_second_half

            clientSocket.send(str('PORT '+ ftp_server_ip_v4_formatted + ',' + port_formatted + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')

            if len(args) == 2:
                directories = args[1]
            else:
                directories = ""

            if resp.decode().startswith("200"):
                clientSocket.send(str('NLST ' + directories + '\r\n').encode('utf-8'))
                newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                newsocket.bind((ftp_server_ip_v4,port))
                newsocket.listen(10)
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
                if resp.decode().startswith("1"):
                    connectionSocket, addr = newsocket.accept()

                    data = b""
                    while True:
                        data_recv = connectionSocket.recv(1024)
                        data += data_recv
                        if not data_recv:
                            break
                        print(data_recv.decode(), end='')

                    size_data = len(data)

                    connectionSocket.close()
                newsocket.close()

                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
                print(f'ftp: {size_data} bytes received in 0.00Seconds veryFast bytes/sec.')
        else :
            print('Not connected.')

    elif commands == 'put':
        if connected:
            if os.path.isfile(os.path.join(os.getcwd(), args[1])):
                ftp_server_ip_v4 = clientSocket.getsockname()[0]
                ftp_server_ip_v4_formatted = ",".join(ftp_server_ip_v4.split('.'))
                port_first_half = random.randint(127,255)
                port_second_half = random.randint(0,255)
                port_formatted = str(port_first_half) + ',' + str(port_second_half)
                port = port_first_half*256 + port_second_half

                clientSocket.send(str('PORT '+ ftp_server_ip_v4_formatted + ',' + port_formatted + '\r\n').encode('utf-8'))
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
                if len(args) == 3:
                    filename = args[2]
                else:
                    filename = args[1]

                if resp.decode().startswith("200"):
                    clientSocket.send(str('STOR ' + filename + '\r\n').encode('utf-8'))
                    newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    newsocket.bind((ftp_server_ip_v4,port))
                    newsocket.listen(10)
                    resp = clientSocket.recv(1024)
                    print(resp.decode(), end='')

                    if resp.decode().startswith("1"):
                        connectionSocket, addr = newsocket.accept()

                        local_path = os.path.join(os.getcwd(), args[1])
                        with open(local_path, 'rb') as file:
                            connectionSocket.sendfile(file)

                        connectionSocket.close()
                    newsocket.close()

                    resp = clientSocket.recv(1024)
                    print(resp.decode(), end='')
                    size_data = os.stat(local_path).st_size
                    print(f'ftp: {size_data} bytes sent in 0.00Seconds veryFast bytes/sec.')
            else:
                print(f'{args[1]}: File not found')
        else :
            print('Not connected.')

    elif commands == 'pwd':
        if connected :
            clientSocket.send(str('XPWD\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'rename':
        if connected :
            clientSocket.send(str('RNFR ' + args[1] + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
            if resp.decode().startswith("350"):
                clientSocket.send(str('RNTO ' + args[2] + '\r\n').encode('utf-8'))
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
        else :
            print('Not connected.')

    elif commands == 'user':
        if connected :
            username = args[1]
            if len(args) == 2:
                password = ""
            else :
                password = args[2]

            clientSocket.send(str('USER '+ username + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
            clientSocket.send(str('PASS '+ password + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
            if resp.decode().startswith("530"):
                print('Login failed.')
        else :
            print('Not connected.')

    elif commands == 'open':
        if connected :
            print(f'Already connected to {hosts}, use disconnect first.')
        else :
            hosts = args[1]
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if len(args) == 3:
                clientSocket.connect((args[1], int(args[2])))
            else :
                clientSocket.connect((args[1], 21))
            resp = clientSocket.recv(1024)

            if resp.decode().startswith("220"):
                print(f"Connected to {args[1]}")
            print(resp.decode(), end='')
            clientSocket.send('OPTS UTF8 ON\r\n'.encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')

            username = input(f'User ({args[1]}:(none)): ')
            clientSocket.send(str('USER '+ username + '\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            if resp.decode().startswith("501"):
                print(resp.decode(), end='')
                print('Login failed.')
            else:
                print(resp.decode(), end='')
                password = getpass('Password: ')
                print()
                clientSocket.send(str('PASS '+ password + '\r\n').encode('utf-8'))
                resp = clientSocket.recv(1024)
                print(resp.decode(), end='')
                if resp.decode().startswith("530"):
                    print('Login failed.')

            connected = True

    elif commands == 'disconnect' or commands == 'close':
        if connected :
            clientSocket.send(str('QUIT\r\n').encode('utf-8'))
            resp = clientSocket.recv(1024)
            print(resp.decode(), end='')
            clientSocket.close()
            connected = False
        else :
            print('Not connected.')
    
    elif commands == "":
        pass
    
    else :
        print('Invalid command.')