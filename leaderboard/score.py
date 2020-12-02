import subprocess
from os import path


def run_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = process.communicate()

    return stdout


def get_diff_lines(working_file):
    command = f"diff -y --suppress-common-lines {working_file} /config/exercicios/vim/resolvido | wc -l"

    return int(run_command(command))


initial_diff_lines = get_diff_lines("/config/base/tonecas")


def file_exists(file_path):
    return path.exists(file_path)


def get_score(user):
    working_file = f"/home/{user}/tonecas"

    if not file_exists(working_file):
        return 0

    diff_lines = get_diff_lines(working_file)

    return 100 * (1 - diff_lines / initial_diff_lines)
