import socket
from threading import Thread, active_count
import json
SIZE = 1024     # buffer size for data transmission
PORT = 50050    # port number for service identification
ENCD = 'utf-8'  # encoding standard

# You can use the following instruction to dynamically obtain the
# IP address of the current local computer, or you can use the
# address 127.0.0.1 that points to the current local computer
# SERVER_IP = socket.gethostbyname(socket.gethostname())
# SERVER_IP = "192.168.100.197"  # you need to use a similar IP address on your PC
SERVER_IP = "localhost"
SOCKET = (SERVER_IP, PORT)  # socket to connect to the server

buffer = []

class TCP_Server():
    def __init__(self, _port, _ip, _size):
        self.sock  = (_ip, _port)  # Socket
        self.bSize = _size         # Buffer size
        self.conn  = None          # Server connection
        self.server()              # Server started

    def server(self):
        print("[SERVER STARTED]")
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(self.sock)

    def accept(self):
        """ The function is returning connection info: conn, ip"""
        return self.conn.accept()

    def listen(self):
        print(f"[LISTENNING] Server is listenning {SERVER_IP}: ")
        self.conn.listen()

    def recv(self, conn):
        """ This function returns received data """
        return conn.recv(self.bSize).decode(ENCD)

    def send(self, conn, msg):
        """ This function is sending one piece of the message. """
        conn.send(msg.encode(ENCD))

    def handler(self, conn, addr):
        global buffer
        """ This function handles every received data. """
        print(f"\n[New Connection] {addr} connected!")
        conect = True
        i = 1
        fullMsg = ""
        while conect:
            try:
                msg = self.recv(conn)
                fullMsg += msg
                if msg:
                    print(f"{addr}: {msg}")
                    # Acknowledge the received message
                    i += 1
                if len(msg) < self.bSize:
                    msgDict = json.loads(fullMsg)
                    if(msgDict["cmd"] == "get-messages"):
                        for msg in buffer:
                            if(msg["to"] == msgDict['from']):
                                self.send(conn,json.dumps(msg))
                                buffer.remove(msg)
                    elif(msgDict["cmd"] == "send"):
                        buffer.append(msgDict)
                    conect = False          # Let define end of the loop
            except:
                connect = False
                pass
        conn.close()

class myServer(TCP_Server):
    def __init__(self, _port=PORT, _ip=SERVER_IP, _size=SIZE):
        super().__init__(_port, _ip, _size)


def main():
    Server  = myServer()
    Server.listen()         # Server is listening to the channel

    while True:
        # Let get current connection info
        curr_conn, curr_ip = Server.accept()
        # Let creta a thread for connection handling
        th = Thread(target=Server.handler, args=(curr_conn, curr_ip))
        th.start()
        print(f"[ACTIVE CONNECTIONS] {active_count() - 1}: ")

if __name__ == '__main__':
    main()