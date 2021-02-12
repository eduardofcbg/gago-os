import asyncio
import logging
import sys
from collections import OrderedDict
from dataclasses import dataclass
from itertools import chain
from operator import itemgetter
from typing import List, Any, Set

from clock import Clock
from score.exercises.score import score


class Periodic:
    pass


@dataclass
class Winning(Periodic):
    users: List


@dataclass
class Setback:
    user: Any


@dataclass
class FinishPlace:
    user: Any
    place: int


@dataclass
class Headstart:
    user: Any


@dataclass
class Win:
    user: Any
    place: int


@dataclass
class Surpass:
    user: Any
    surpassed: Set


def winning_users(scores):
    max_score = max(scores.values())
    return [user for user, score in scores.items() if score > 0 and score == max_score]


def create_periodic(scores, clock):
    if clock.is_multiple_of(minutes=20):
        yield Winning(users=winning_users(scores))


def count_finish(notifications):
    return sum(
        1
        for notification in notifications
        if isinstance(notification, (Win, FinishPlace))
    )


def count_headstart(notifications):
    return sum(
        1 for notification in notifications if isinstance(notification, Headstart)
    )


def create_user_to_place(scores):
    dsc_users = sorted(scores.items(), key=itemgetter(1), reverse=True)
    user_to_place = OrderedDict()

    for place, (user, score) in enumerate(dsc_users):
        user_to_place[user] = place

    return user_to_place


def create_progress(new_scores, previous_scores, acc_notifications):
    new_users_to_place = create_user_to_place(new_scores)
    previous_users_to_place = create_user_to_place(previous_scores)
    previous_users_dsc = list(previous_users_to_place)

    for user, new_place in new_users_to_place.items():
        score = new_scores[user]
        previous_score = previous_scores[user]
        previous_place = previous_users_to_place[user]

        surpassed = {
            surpassed_user
            for surpassed_user in previous_users_dsc[new_place:previous_place]
            if score != new_scores[surpassed_user]
        }

        if surpassed:
            yield Surpass(user=user, surpassed=surpassed)

        if score < previous_score:
            yield Setback(user)

        if previous_score < 100 and score == 100:
            place = count_finish(acc_notifications) + 1
            if place <= 3:
                yield Win(user=user, place=place)
            else:
                yield FinishPlace(user=user, place=place)

        if previous_score == 0 and score > 0 and score != 100:
            if count_headstart(acc_notifications) == 0:
                yield Headstart(user=user)


async def pull_notifications(exercise, users=None):
    clock = Clock()
    clock.set_delta(seconds=10)
    clock.start()

    acc_notifications = []
    previous_scores = None

    while True:
        try:
            new_scores = await score(exercise, users)

            progress = create_progress(
                new_scores, previous_scores or new_scores, acc_notifications
            )
            periodic = create_periodic(new_scores, clock)
            notifications = list(chain(progress, periodic))

            for notification in notifications:
                yield notification

            acc_notifications = [*acc_notifications, *notifications]
            previous_scores = new_scores
        except IOError as e:
            logging.exception(e)
        finally:
            await asyncio.sleep(clock.sleep_time())

            clock.tick()


async def print_notifications(exercise):
    async for notification in pull_notifications(exercise):
        print(notification)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Must specify exercise. For example 'navigation.py scripting'.")

    exercise = sys.argv[1]

    asyncio.run(print_notifications(exercise))
