from score.execute.local import run_command


def run_script(work_dir):
    command = f"{work_dir}/scripting2"

    return run_command(command)

script_out_goal = 


def score(user):
    work_dir = f"/home/{user}"
    script_out = run_script(work_dir)

    if error_count > max_number_errors:
        raise ValueError(f"Found {work_dir} errors, than expected {max_number_errors}")

    return int(100 * (1 - error_count / max_number_errors))
