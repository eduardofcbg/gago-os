import subprocess
from os import path


def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        executable="/bin/bash",
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(stderr)

    return stdout


def file_exists(file_path):
    return path.exists(file_path)
