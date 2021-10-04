import socket 



i = 0
while(i<100):
    i+=1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((socket.gethostname(), 1239))
    how_many_bytes_to_receive = 8
    msg = s.recv(how_many_bytes_to_receive)
    msg_encoding = "utf-8"
    print(msg.decode(msg_encoding))
