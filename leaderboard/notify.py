import sys
import asyncio
from dataclasses import dataclass
from typing import Set
from itertools import chain

from utils import run_in_executor
from exercises.score import score
from clock import Clock


@dataclass
class Winning:
    users: Set[str]


@dataclass
class Setback:
    user: str


@dataclass
class FinishPlace:
    user: str
    place: int


@dataclass
class Headstart:
    user: str


@dataclass
class Win:
    user: str
    place: int


def create_periodic(new_scores, clock):
    def is_current_minute_multiple_of(*, minutes):
        return (
            clock.current_tick != 0
            and clock.current_tick % clock.tick_for(minutes=minutes) == 0
        )

    def winning_users():
        max_score = max(new_scores.values())
        return [
            user
            for user, score in new_scores.items()
            if score > 0 and score == max_score
        ]

    if is_current_minute_multiple_of(minutes=20):
        yield Winning(users=set(winning_users()))


def create_progress(new_scores, previous_scores, acc_notifications):
    def count_finish():
        return sum(
            1
            for notification in acc_notifications
            if isinstance(notification, (Win, FinishPlace))
        )

    def count_headstart():
        return sum(
            1
            for notification in acc_notifications
            if isinstance(notification, Headstart)
        )

    for user, score in new_scores.items():
        previous_score = previous_scores[user]

        if score < previous_score:
            yield Setback(user)

        if previous_score < 100 and score == 100:
            place = count_finish() + 1
            if place <= 3:
                yield Win(user=user, place=place)
            else:
                yield FinishPlace(user=user, place=place)

        if previous_score == 0 and score > 0 and score != 100:
            if count_headstart() == 0:
                yield Headstart(user=user)


@run_in_executor
def score_async(exercise):
    return score(exercise)


async def pull_notifications(exercise):
    clock = Clock()
    clock.set_delta(seconds=5)
    clock.start()

    acc_notifications = []
    previous_scores = None

    while True:
        new_scores = await score_async(exercise)

        progress = create_progress(
            new_scores, previous_scores or new_scores, acc_notifications
        )
        periodic = create_periodic(new_scores, clock)
        notifications = list(chain(progress, periodic))

        for notification in notifications:
            yield notification

        acc_notifications = [*acc_notifications, *notifications]
        previous_scores = new_scores

        await asyncio.sleep(clock.get_delta_seconds() + clock.lag())
        clock.tick()


async def print_notifications(exercise):
    async for notification in pull_notifications(exercise):
        print(notification)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(
            f"Must specify exercise. For example 'navigation.py scripting1'."
        )

    exercise = sys.argv[1]

    asyncio.run(print_notifications(exercise))
