import asyncio

from score.exercises.vim import score as score_vim
from score.exercises.navigation import score as score_navigation
from score.exercises.scripting1.score import score as score_scripting1
from score.exercises.scripting2.score import score as score_scripting2
from score.exercises.http_server.score import score as score_http_server
from users import get_users

score_exercise_sync = {
    "vim": score_vim,
    "navigation": score_navigation,
    "scripting1": score_scripting1,
    "scripting2": score_scripting2,
}

score_exercise_async = {"http_server": score_http_server}


def is_valid_exercise(exercise):
    return exercise in score_exercise_sync or exercise in score_exercise_async


async def score(exercise, users=None):
    users = users or get_users()

    if not is_valid_exercise(exercise):
        raise ValueError(
            f"Exercise {exercise} does not exist in {set(score_exercise_sync).union(score_exercise_async)}"
        )

    if exercise in score_exercise_async:
        score_fn = score_exercise_async[exercise]
        scores = await asyncio.gather(*map(score_fn, users))

        return dict(zip(users, scores))
    else:
        score_fn = score_exercise_sync[exercise]

        return dict(zip(users, map(score_fn, users)))
