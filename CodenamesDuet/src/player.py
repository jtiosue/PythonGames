import socket
from threading import Thread
import tkinter as tk
from ui import Display


def recv(clientsocket, display):
    while True:
        msg = clientsocket.recv(8192).decode()
        print('\a')
        display.recv(msg)
        
def create_clientsocket():
    hostname = input("Enter hostname/IP to connect to: ")
    port = int(input("Enter port: "))
    
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((hostname, port))
    return clientsocket

def main():
    clientsocket = create_clientsocket()
    root = tk.Tk()
    display = Display(clientsocket, root)
    display.pack()
    
    thread_recv = Thread(target=recv, args=(clientsocket, display))
    thread_recv.start()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
