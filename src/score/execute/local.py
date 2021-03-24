from subprocess import Popen, PIPE


def run_command(command, cwd=None):
    try:
        process = Popen(
            command, stdout=PIPE, stderr=PIPE, shell=True, executable="/bin/bash", cwd=cwd
        )
        stdout, stderr = process.communicate()
    except OSError as e:
        raise IOError(e)

    if stderr:
        raise RuntimeError(stderr)

    return stdout
