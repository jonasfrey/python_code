import os
import sys
import socket

import subprocess
subprocess.Popen(["rm","-r","some.file"])

def f_popen_subprocess(s_command):
    print('f_popen_subprocess: ' +s_command)
    subprocess.Popen(s_command.split(' '))


def f_b_port_open(s_ip, n_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((s_ip,n_port))
    b = False
    if result == 0:
        p = True
    else:
        p = False
    sock.close()
    return b

def f_execute_command(
    s_command
):
    print('f_execute_command: ' +s_command)
    stream = os.popen(s_command)
    # print(stream)
    s = stream.read()
    s += stream.read()
    return stream.read()

n_port = 5050
s_ip = '170.17.146.34'

# print(f_b_port_open(s_ip, n_port))

s_command = f"telnet {s_ip} {n_port}"
f_popen_subprocess(s_command)

n_i =1
while(n_i < 10000):
    print(n_i)
    n_i +=1
    n_port = n_i
    s_command = f"telnet {s_ip} {n_port}"
    # s_command_output = f_execute_command(s_command)
    f_popen_subprocess(s_command)
    # print(s_command_output)