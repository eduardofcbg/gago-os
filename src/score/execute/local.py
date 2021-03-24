from subprocess import Popen, PIPE


def run_command(command, cwd=None):
    process = Popen(
        command, stdout=PIPE, stderr=PIPE, shell=True, executable="/bin/bash", cwd=cwd
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(stderr)

    return stdout
