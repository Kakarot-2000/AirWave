from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(bufsize).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    #Handles sending of messages
    msg = my_msg.get()
    my_msg.set("")  # clearing input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chat App")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Enter message here ")
scrollbar = tkinter.Scrollbar(messages_frame)

# To contain all the messages
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

host = '192.168.43.211'
port = 33000
bufsize = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((host,port))

receive_thread = Thread(target=receive)
receive_thread.start()
# Starts GUI execution
tkinter.mainloop()
