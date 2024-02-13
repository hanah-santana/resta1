import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
