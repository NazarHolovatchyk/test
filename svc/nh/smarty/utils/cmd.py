import subprocess


def exec_command(command):
    """
    Execute the command and return the exit status.
    """
    pobj = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    stdout, stderr = pobj.communicate()

    exit_code = pobj.returncode
    if exit_code != 0:
        raise IOError("Command '{}' failed: {} \n {}".format(command, stdout, stderr))

    return stdout, stderr
