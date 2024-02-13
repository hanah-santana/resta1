import socket
import threading
import sys
from random import randint
import time

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

if __name__ == "__main__":
    server = Server()
    server.run()