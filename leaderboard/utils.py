import asyncio
from functools import wraps, partial
from subprocess import Popen, PIPE
from os import path


def run_command(command):
    process = Popen(
        command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        executable="/bin/bash",
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(stderr)

    return stdout


def file_exists(file_path):
    return path.exists(file_path)


def dir_exists(dir_path):
    return path.isdir(dir_path)


def run_in_executor(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, partial(f, *args, **kwargs))

    return wrapped
