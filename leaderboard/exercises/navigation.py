from utils import run_command, file_exists


def get_diff_lines(dir1, dir2):
    command = f"diff -y --suppress-common-lines <(find {dir1} ! -name '.*' -printf '%P\n' | sort) <(find {dir2} ! -name '.*' -printf '%P\n' | sort) | wc -l"

    return int(run_command(command))


solved_dir = "/config/exercicios/navigation/resolvido"
max_diff_lines = 13


def get_score(user):
    work_dir = f"/home/{user}/navegacao"

    if not file_exists(work_dir):
        return 0

    diff_lines = get_diff_lines(work_dir, solved_dir)
    score = 100 * (1 - diff_lines / max_diff_lines)

    return max(score, 1)
