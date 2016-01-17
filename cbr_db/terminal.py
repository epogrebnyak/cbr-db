import subprocess
import time


def terminal(shell_command_string):
    print("\nCalling:")
    print(shell_command_string, "")
    start_time = time.time()
    subprocess.check_call(shell_command_string, shell=True)
    print("Elapsed time:", round(time.time() - start_time, 2))
