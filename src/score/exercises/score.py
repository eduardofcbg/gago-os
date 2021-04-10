import logging
import asyncio

from utils import run_in_executor
from score.exercises.vim import score as score_vim
from score.exercises.navigation import score as score_navigation
from score.exercises.scripting1.score import score as score_scripting1
from score.exercises.scripting2.score import score as score_scripting2
from score.exercises.http_server.score import score as score_http_server
from users import get_users as get_os_users

score_exercise_sync = {
    "vim": score_vim,
    "navigation": score_navigation,
    "scripting1": score_scripting1,
    "scripting2": score_scripting2,
}


score_exercise_async = {"http_server": score_http_server}


@run_in_executor
def score_sync(score_fn, users):
    def _score_return_exception(user):
        try:
            return score_fn(user)
        except Exception as e:
            return e

    return dict(zip(users, map(_score_return_exception, users)))


def score_async(score_fn, users):
    return asyncio.gather(*map(score_fn, users), return_exceptions=True)


def is_valid_exercise(exercise):
    return exercise in score_exercise_sync or exercise in score_exercise_async


async def score(exercise, users=None):
    users = users or get_os_users()

    if not is_valid_exercise(exercise):
        raise ValueError(
            f"Exercise {exercise} does not exist in {set(score_exercise_sync).union(score_exercise_async)}"
        )
        
    if exercise in score_exercise_async:
        score_fn = score_exercise_async[exercise]

        user_result =  await score_async(score_fn, users)
    else:
        score_fn = score_exercise_sync[exercise]

        user_result =  score_sync(score_fn, users)

    user_score = {}

    for user, result in user_score.items():
        if isinstance(result, Exception):
            ex = result
            logging.exception(ex)
        else:
            score = result
            user_score[user] = score

    return user_score
 
