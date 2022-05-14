import os 
import subprocess


# a_s_video_device = os.system("ls /dev/video*")

# process = subprocess.Popen(
#     ["ls", "/dev/video*"],
#     stdout=subprocess.PIPE, 
#     text=True
#     )
# # run bash command

# s_command_output, error = process.communicate()

# process = subprocess.check_output(
#     ["ls", "/dev/video*"],
#     )

a_s_video_device = os.popen("ls /dev/video*").read()

# a_s_video_device = os.execvp("ls /dev/video*")
print(str(a_s_video_device).split("\n"))

exit()