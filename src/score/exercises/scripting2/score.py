from score.execute.local import run_command


def run_score_script(work_dir):
    command = f"/src/score/exercises/scripting2/score.sh {work_dir}"

    try:
    	return int(run_command(command))
    except ValueError:
    	return 0

def get_max_score():
    return 17 


def score(user):
    work_dir = f"/home/{user}"

    return int(run_score_script(work_dir) / get_max_score() * 100)

