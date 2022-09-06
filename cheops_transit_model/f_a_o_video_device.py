import os
from O_video_device import O_video_device 

def f_run_command(s_command): 
    print("f_run_command "+ s_command)
    # s_output = os.system(s_command)
    # return s_output
    stream = os.popen(s_command)
    s = stream.read()
    print(s)
    return s

def f_a_o_video_device():

    s_command = "v4l2-ctl --list-devices"
    s_output = f_run_command(s_command)
    s_search = "/dev/video"
    a_s_line = s_output.split("\n")
    o_video_device = False
    a_o_video_device = []
    for s_line in a_s_line:
        # print(s_line)
        if((s_line.strip()) == ''):
            continue

        if(s_search in s_line):
            if(o_video_device):
                o_video_device.a_n_number.append(s_line.strip()[len(s_search):])
        else: 
            if ("/dev" in s_line) == False:
                if o_video_device:
                    a_o_video_device.append(o_video_device)
                # print(s_line)
                o_video_device = O_video_device([],s_line.strip())

    if(not o_video_device in a_o_video_device):
        a_o_video_device.append(o_video_device)
    # print(s_output)
    # print("end")

    return a_o_video_device


if __name__ == "__main__":
    a_o_video_device = f_a_o_video_device()
    print(a_o_video_device)