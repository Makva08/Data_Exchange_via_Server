import socket
from threading import Thread
import json
import time

SIZE = 1024     # buffer size for data transmission
PORT = 50050    # port number for service identification
ENCD = 'utf-8'  # encoding standard

# You can use the following instruction to dynamica lly obtain the
# IP address of the current local computer, or you can use the
# address 127.0.0.1 that points to the current local computer
# SERVER_IP = socket.gethostbyname(socket.gethostname())
# SERVER_IP = "192.168.100.197"  # you need to use a similar IP address on your PC
SERVER_IP = "localhost"
SOCKET = (SERVER_IP, PORT)  # socket to connect to the server

class TCP_Client:
    def __init__(self, _username,_port, _ip, _size):
        self.username = _username
        self.sock  = (_ip, _port)  # Socket
        self.bSize = _size         # Buffer size
        self.conn  = None          # Client connection
        self.client()              # Client started

    def client(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(1)
        self.conn.connect(self.sock)

    def decodeMessage(self,msg = "{}"):
        """ This function returns received data """
        message = json.loads(msg)
        return f"{message['from']}: {message['msg']}"

    def send(self, cmd,msg = "",dest = ""):
        self.client()
        """ This function is sending one piece of the message. """
        payload = {
            "cmd":cmd,
            "from":self.username,
            "to":dest,
            "msg":msg
        }
        self.conn.send(json.dumps(payload).encode(ENCD))

    def sender(self):
        while 1:
            username = input("Enter receivers username: ")
            message = input("Enter message: ")
            self.send(cmd = "send",msg = message,dest = username)
            self.receiver()

    def receiver(self):
        self.send("get-messages")
        connect = True
        fullMsg = ""
        while connect:
            try:
                msg = self.conn.recv(self.bSize)
                msg = msg.decode(ENCD)
                fullMsg += msg
                if(len(msg) < self.bSize):
                    connect = False
                    if len(fullMsg) > 0:
                        print("")
                        print(self.decodeMessage(fullMsg))
            except:
                pass

class myClient(TCP_Client):
    def __init__(self, username,_port=PORT, _ip=SERVER_IP, _size=SIZE):
        super().__init__(username,_port, _ip, _size)




def main():
    username = input("Enter username: ")
    client  = myClient(username)
    recvClient  = myClient(username)

    th = Thread(target=th.sender)

    th.start()

if __name__ == '__main__':
    main()