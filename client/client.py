import socket
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        inpt = input()
        s.sendall(inpt.encode())
        data = s.recv(1024)
        print('Received', repr(data))