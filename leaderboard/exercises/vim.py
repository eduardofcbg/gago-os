from utils import run_command, file_exists


def get_diff_lines(working_file):
    command = f"diff -y --suppress-common-lines {working_file} /config/exercicios/vim/resolvido | wc -l"

    return int(run_command(command))


max_diff_lines = get_diff_lines("/config/base/tonecas")


def get_score(user):
    working_file = f"/home/{user}/tonecas"

    if not file_exists(working_file):
        return 0

    diff_lines = get_diff_lines(working_file)
    score = 100 * (1 - diff_lines / max_diff_lines)

    return max(score, 1)