from tkinter import *
from tkinter import messagebox
import tkinter as tk
from server import Client
from tkinter import scrolledtext, Entry, Button
import threading

window = Tk()
window.title("PPD | Resta1")
window.geometry('1200x800')
reset_functions = []

def give_up():
    message = "O oponente desistiu do jogo e foi desconectado"
    client.sock.send(message.encode('utf-8'))
    client.disconnect()
    chat_history.insert(END, "Você está desconectado do servidor, as mensagens não chegarão ao oponente")
    messagebox.showerror("","Você Desistiu\nO oponente venceu o jogo")
    #Game STATE: Finalized/Defeated

give_up_button = Button(window, text="Desistir do Jogo", font=("Helvetica", 16), height=2, width=15, bg="SystemButtonFace", command=give_up).place(x= 100, y=600)

chat_frame = Frame(window)
chat_frame.place(x= 30, y=100)

chat_history = scrolledtext.ScrolledText(chat_frame, wrap=WORD, width=40, height=30)
chat_history.pack()

entry_field = Entry(chat_frame, width=25)
entry_field.pack()

host = '127.0.0.1'
port = 8080
client = Client(host, port)

def receive_messages():
        while True:
            try:
                message = client.sock.recv(1024).decode('utf-8')
                chat_history.insert(tk.END, 'Oponente: '+ message + '\n')
            except:
                break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def send_message():
    message = entry_field.get()
    if message:
        chat_history.insert(END, "You: " + message + "\n")
        client.sock.send(message.encode('utf-8'))
        entry_field.delete(0, END)

send_button = Button(chat_frame, text="Send", command=send_message)
send_button.pack()

window.mainloop()