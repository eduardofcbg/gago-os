from os import path
from functools import lru_cache

from score.execute.local import run_command


def get_diff_lines(working_file):
    command = f"diff -y --suppress-common-lines {working_file} /config/exercicios/vim/resolvido | wc -l"

    return int(run_command(command))


@lru_cache(maxsize=None)
def get_max_diff_lines():
    return get_diff_lines("/config/base/tonecas")


def score(user):
    working_file = f"/home/{user}/tonecas"

    if not path.exists(working_file):
        return 0

    diff_lines = get_diff_lines(working_file)
    score = int(100 * (1 - diff_lines / get_max_diff_lines()))

    return max(score, 1)
