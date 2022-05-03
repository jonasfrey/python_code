import subprocess
import time
import os
import rawpy
import cv2

def f_run_bash_command(a_binary_and_arguments, b_output_is_text = False):
    print("running bash command:")
    print(" ".join(a_binary_and_arguments))
    process = subprocess.Popen(
        a_binary_and_arguments,
        stdout=subprocess.PIPE, 
        text=b_output_is_text
        )
    # run bash command

    s_command_output, error = process.communicate()

    # print(error)
    # print(str(s_command_output))

    return s_command_output


def f_detect_cameras():
    s_command_output = f_run_bash_command(['gphoto2', '--auto-detect'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)
    # print(len(a_lines))
    if(len(a_lines) < 4):
        print('no cameras detected ! ')
    
def f_list_config():
    s_command_output = f_run_bash_command(['gphoto2', '--list-config'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_read_config(s_name):
    s_command_output = f_run_bash_command(['gphoto2', '--get-config', s_name], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_write_config_index(s_name, s_value):
    s_command_output = f_run_bash_command(['gphoto2', '--set-config', s_name+'='+str(s_value)], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)

def f_write_config_value(s_name, s_value):
    s_command_output = f_run_bash_command(['gphoto2', '--set-config-value', s_name+'="'+str(s_value)+'"'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_capture_and_download(
    s_path_file_name
):
    try:
        os.remove(s_path_file_name)
    except:
        pass
    s_command_output = f_run_bash_command(['gphoto2','--capture-image-and-download', '--filename', str(s_path_file_name)], True)

    a_lines = s_command_output.split("\n")
    print(s_command_output)

def f_n_ts_ms():
    return round(time.time() * 1000)

    
if __name__ == '__main__':
        
    s_path_file_name = "./tmp.arw"

    print("f_detect_cameras")
    f_detect_cameras()

    print("f_list_config")
    f_list_config()

    print("read config shutterspeed")
    f_read_config("shutterspeed")

    # print("write config shutterspeed to 1")
    # f_write_config_value("/main/capturesettings/shutterspeed", 1)

    print("write config shutterspeed to index 23:'1/6'")
    f_write_config_index("/main/capturesettings/shutterspeed", 23)

    n_i = 0
    n_ts = f_n_ts_ms()
    n_ts_last = f_n_ts_ms()
    n_ts_delta = f_n_ts_ms()

    f_capture_and_download(s_path_file_name)
    o_img_raw = rawpy.imread(s_path_file_name)
    cv2.imshow('image',o_img_raw.raw_image)

    # while(n_i < 3):
    #     n_ts = f_n_ts_ms()
    #     n_ts_delta = n_ts - n_ts_last
    #     print("delta milliseconds:")
    #     print(n_ts_delta)


    #     n_i+=1
    #     n_ts_last = n_ts

    print("end of main.py")


