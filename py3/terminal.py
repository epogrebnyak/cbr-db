import subprocess
import time
import os

def terminal(shell_command_string):
    print("\nCalling:")
    print(shell_command_string, "")
    try:
        start_time = time.time()
        subprocess.call(shell_command_string, shell=True)
        elapsed_time = time.time() - start_time
    except subprocess.CalledProcessError:
        os.exit("\nCannot execute the program {}\n".format(shell_command_string))

    print("Elapsed time:", round(elapsed_time, 2))

if __name__ == '__main__':
    terminal("ping google.com")
    terminal("echo Hello!")
