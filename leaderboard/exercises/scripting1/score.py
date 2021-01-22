from utils import run_command


def count_errors(work_dir):
    command = f"/leaderboard/exercises/scripting1/errorlog.sh {work_dir} | wc -l"

    return int(run_command(command))

max_number_errors = 12

def get_score(user):
    work_dir = f"/home/{user}/scripting1"

    return int(100 * (1 - count_errors(work_dir) / max_number_errors))

