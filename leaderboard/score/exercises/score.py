from score.exercises.navigation import score as score_navigation
from score.exercises.scripting import score as score_scripting
from score.exercises.vim import score as score_vim
from users import get_users

score_exercise = {
    "vim": score_vim,
    "navigation": score_navigation,
    "scripting": score_scripting,
}


def is_valid_exercise(exercise):
    return exercise in score_exercise


def score(exercise, users=None):
    if not is_valid_exercise(exercise):
        raise ValueError(f"Exercise {exercise} does not exist in {set(score_exercise)}")

    return {user: score_exercise[exercise](user) for user in users or get_users()}
