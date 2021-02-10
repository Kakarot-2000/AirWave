from threading import Thread
import socket as sc1
from socket import AF_INET, socket, SOCK_STREAM
import tkinter as tk
import sys


clients = {}
addresses = {}
bufsize = 1024


def accept_connections():
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    
    host = sc1.gethostbyname(sc1.gethostname())         #'127.0.0.1'
    print('Hosted on ',host)
    port = 33000
    
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host,port))
    print("socket binded to port : ",port)

    s.listen(5)
    print("Waiting for connection...")

    while True:
        c,address = s.accept()
        print("Connected to : ",address[0]," : ",address[1])
        c.send(bytes("Welcome! Now type your name and press enter!", "utf8"))
        addresses[c] = address
        Thread(target=handle_client,args=(c,)).start()
        
    s.close()


def handle_client(c):  # Takes client socket as argument.
    #Handles a single client connection

    name = c.recv(bufsize).decode("utf8")
    welcome_text = 'Welcome {}! If you ever want to quit, type quit to exit.'.format(name)
    c.send(bytes(welcome_text, "utf8"))
    msg = "{} has joined the chat!".format(name)
    broadcast(bytes(msg,"utf8"))
    clients[c] = name

    while True:
        msg = c.recv(bufsize)
        if msg!=bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            c.send(bytes("{quit}", "utf8"))
            c.close()
            del clients[c]
            broadcast(bytes("{} has left the chat.".format(name), "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    #Broadcasts a message to all the clients

    for sock in clients:
        print(sock)
        sock.send(bytes(prefix, "utf8")+msg)


def stop_server():
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    sys.exit()

top = tk.Tk()
top.title("Server")
top.config(bg='#3D3C3A')
top.geometry('256x64')


# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
frame = tk.Frame(top)
btnStart = tk.Button(frame, text="Connect", command=lambda : accept_connections())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(frame, text="Stop", command=lambda : stop_server())
btnStop.pack(side=tk.LEFT)
frame.pack(side=tk.TOP, pady=(10, 0))
frame2 = tk.Frame(top)
lblHost = tk.Label(frame2, text = "Host: {}".format(sc1.gethostbyname(sc1.gethostname())))
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(frame2, text = "Port: 1234 ")
lblPort.pack(side=tk.LEFT)
frame2.pack(side=tk.TOP, pady=(5, 0))



top.mainloop()
