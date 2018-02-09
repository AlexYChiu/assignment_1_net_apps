"""
    Server side of Assignment 1 for ECE 4564.
    Handles:
    1. Receiving question from client. 
    2. Speaking question. 
    3. Sending a receiving from WolframAlpha API.
    4. Sending answer to client. 
"""

import sys
import argparse
import socket 

parser = argparse.ArgumentParser(description='Prossesses arguments for client.')
parser.add_argument('-p', help='Set the server port.')
parser.add_argument('-b', help='Set the backlog size.')
parser.add_argument('-z', help='Set the socket size')

args = parser.parse_args()

if args.p == None:
    print('Please set server port with the -p flag.')
    sys.exit(1)
if args.b == None:
    print('Please set backlog size with the -b flag.')
    sys.exit(1)
if args.z == None:
    print('Please set socket size with the -z flag.')
    sys.exit(1)

host = 'localhost'

try:
    port =      int(args.p)
    backlog =   int(args.b)
    size =      int(args.z)
except Exception as ex:
    print(ex)
    sys.exit(1)

print('Starting server on port ' + str(port) + '...')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))  
s.listen(backlog)

print('Starting server on port ' + str(port) + '...')

# Simple echo server for now.
while 1:
    client, address = s.accept()     
    data = client.recv(size)    
    if data: 
        print('FOUND DATA: ' + data)        
        client.send(data)   
        client.close()  


print('Finished')