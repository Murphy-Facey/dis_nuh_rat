# Dis Nuh Rat

This is a remote access trojan made in python

## How to run 

First install opencv

Download the wheel for [pyHook](). Then navigate to where the .whl file is, and run the following command to install it.

```
pip install pyHook-1.5.1-cp37-cp37m-win_amd64.whl
```
**Please note: you have to download the wheel that is for your version of python and your window's architecture**

Depending on your version of Windows, numpy may not work. If so, uninstall and re-install it but a older version than the one that was installed. Use the following command

```
pip uninstall numpy
pip install --upgrade nupmy==1.19.3
```

**Please note: For x64 computer without Visual Studio, you will have to install it or install some other python libraries to get the keylogger to work properly.**

Install opencv 

```bash
pip install opencv-contrib-python --upgrade
pip install opencv-python  
```

Then run the server followed by the client
```cmd
# run the server
python server.py

# and in another terminal (or machine), run the client
python client.py 
```