import socket
import threading
import sys
from random import randint
import time

import tkinter as tk
from tkinter import scrolledtext, Entry, Button

class p2p:
    peers = ['127.0.0.1']

class Server:
    
    connections = []
    peers = []
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.input_payload = []
        
        self.sock.bind(('127.0.0.1',8080))
        self.sock.listen(1)
  
        print("Server running")
            
    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target = self.handler, args = (c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]),"Connected")
            self.sendPeers()
        
    def handler(self, c, a):
        while True:
            try:
                data = c.recv(1024)
            except:
                data = None
            
            if not data:
                print(str(a[0]) + ':' + str(a[1]),"Disconected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break
            
            print(str(data,'utf-8'))
            self.input_payload.append(str(data,'utf-8'))
            
            for connection in self.connections:
                if connection.getpeername()[1] != a[1]:
                    connection.send(data)
                
    def sendPeers(self):
        p = ""
        
        for peer in self.peers:
            p = p + peer + ","
            
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p,"utf-8"))

    def send_message(self,data):
        #while True:
        #data = bytes(input(""), 'utf-8')
        try:
            for connection in self.connections:
                connection.send(bytes(data, 'utf-8'))
                #sock.send(bytes(input(""), 'utf-8'))
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print("Failed to send message: %s" % str(e))

class Client:
            
    def __init__(self, address,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((address,port))
        self.input_payload = []
      
    def run(self):
        while True:
            data = self.sock.recv(1024)
            
            if not data:
                break
            
            if data[0:1] == b'\x11':
                print("Got peers")
                self.updatePeers(data[1:])
                
            else:
                print(str(data,'utf-8'))
                self.input_payload.append(str(data,'utf-8'))
    def updatePeers(self,peerData):
        p2p.peers = str(peerData,"utf-8").split(",")[:-1]
        self.peers = p2p.peers
        
    def disconnect(self):
        self.sock.close()
        print("Disconnected from server")

if __name__ == "__main__":
    server = Server()
    server.run()