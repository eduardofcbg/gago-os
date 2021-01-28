from users import get_users
from exercises.vim import score as score_vim
from exercises.navigation import score as score_navigation
from exercises.scripting1.score import score as score_scripting1


score_exercise = {
    "vim": score_vim,
    "navigation": score_navigation,
    "scripting1": score_scripting1,
}


def is_valid_exercise(exercise):
    return exercise in score_exercise


def score(exercise):
    if not is_valid_exercise(exercise):
        raise ValueError(
            f"Exercise {exercise} does not exist in {set(score_exercise)}"
        )

    return {user: score_exercise[exercise](user) for user in get_users()}
