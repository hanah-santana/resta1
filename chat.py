from tkinter import *
from tkinter import messagebox
import tkinter as tk
from client import Client
from tkinter import scrolledtext, Entry, Button
import threading


# Create the main window
window = Tk()
window.title("PPD | Tic-Tac-Toe")
window.geometry('1000x800')
reset_functions = []

give_up_button = Button(window, text="Desistir do Jogo", font=("Helvetica", 16), height=2, width=15, bg="SystemButtonFace",
                      command="").place(x= 700, y=40)

chat_frame = Frame(window)
chat_frame.place(x= 680, y=100)

chat_history = scrolledtext.ScrolledText(chat_frame, wrap=WORD, width=30, height=15)
chat_history.pack()

entry_field = Entry(chat_frame, width=25)
entry_field.pack()

host = '127.0.0.1'
port = 8080
client = Client(host, port)

def receive_messages():
        while True:
            try:
                message = client.client_socket.recv(1024).decode('utf-8')
                chat_history.insert(tk.END, 'Oponente: '+ message + '\n')
            except:
                break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def send_message():
    message = entry_field.get()
    if message:
        chat_history.insert(END, "You: " + message + "\n")
        client.client_socket.send(message.encode('utf-8'))
        entry_field.delete(0, END)

send_button = Button(chat_frame, text="Send", command=send_message)
send_button.pack()

def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_display.insert(tk.END, 'Oponente: '+ message + '\n')
            except:
                break

window.mainloop()