from os import path
from score.execute.local import run_command


def get_diff_lines(dir1, dir2):
    command = f"diff -y --suppress-common-lines <(find {dir1} ! -name '.*' -printf '%P\n' | sort) <(find {dir2} ! -name '.*' -printf '%P\n' | sort) | wc -l"

    return int(run_command(command))


solved_dir = "/config/exercicios/navigation/resolvido"
max_diff_lines = 13


def score(user):
    work_dir = f"/home/{user}/navigation"

    if not path.isdir(work_dir):
        return 0

    diff_lines = get_diff_lines(work_dir, solved_dir)
    score = int(100 * (1 - diff_lines / max_diff_lines))

    return max(score, 1)
