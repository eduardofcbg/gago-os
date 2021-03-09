from subprocess import Popen, PIPE


def run_command(command):
    process = Popen(
        command, stdout=PIPE, stderr=PIPE, shell=True, executable="/bin/bash"
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(stderr)

    return stdout
