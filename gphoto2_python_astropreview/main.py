import subprocess




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


def f_capture_and_download():
    s_command_output = f_run_bash_command(['gphoto2','--capture-image-and-download'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)

    
if __name__ == '__main__':

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

    f_capture_and_download()

    print("end of main.py")


