import os
import sys



def f_execute_command(
    s_command
):
    print('f_execute_command: ' +s_command)
    stream = os.popen(s_command)
    return stream.read()

s_ip_or_domain = 'google.com'
s_command_tracert = f"traceroute {s_ip_or_domain}"

print(os.argv)
s_output = f_execute_command("echo test")
print(s_output)