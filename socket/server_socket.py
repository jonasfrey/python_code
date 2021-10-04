import socket 

# what is a socket

# socket is the endpoint that reccceives data, 
# socket can send data
# socket can receiv data
# socket has ip and port

## socket.AF_INET -> ipv4
# socket.SOCK_STREAM -> tcp 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_hostname = socket.gethostname()
s_port = 1239
s.bind((s_hostname, s_port))
server_queue = 5
s.listen(server_queue) # this server will listen


# listen forever

while True: 
    # clientsocket = s.accept()[0]
    # address = s.accept()[1]

    clientsocket, address = s.accept()

    print("Connection from "+str(address)+" has been established!")
    # byte_type = "utf-8" wont somehow work in bytes("...", byte_type) -> TypeError: str() takes at most 1 argument (2 given)
    clientsocket.send(0b00000001)