import sys
import asyncio
from dataclasses import dataclass
from typing import List

from utils import run_in_executor
from exercises.score import score
from clock import Clock


@dataclass
class Winning:
    users: List[str]


@dataclass
class Setback:
    user: str


@dataclass
class Finish:
    user: str


@dataclass
class FinishPlace:
    user: str
    place: int


@dataclass
class Start:
    user: str


@dataclass
class Headstart:
    user: str


@dataclass
class Win:
    user: str
    place: int


def create_progress_notifications(new_scores, previous_scores, clock):
    def is_current_minute_multiple_of(*, minutes):
        return (
            clock.current_tick != 0
            and clock.current_tick % clock.tick_for(minutes=minutes) == 0
        )

    def winning_users():
        max_score = max(new_scores.values())
        return [
            user
            for (user, score) in new_scores.items()
            if score > 0 and score == max_score
        ]

    if is_current_minute_multiple_of(minutes=20):
        yield Winning(users=winning_users())

    for (user, score) in new_scores.items():
        previous_score = previous_scores[user]

        if score < previous_score:
            yield Setback(user)

        if previous_score < 100 and score == 100:
            yield Finish(user)

        if previous_score == 0 and score > 0 and score != 100:
            yield Start(user)


def create_notifications(acc_notifications, new_scores, previous_scores, clock):
    def count_finish(notifications):
        return sum(
            1 for notification in notifications if isinstance(notification, Finish)
        )

    def count_start(notifications):
        return sum(
            1 for notification in notifications if isinstance(notification, Start)
        )

    for notification in create_progress_notifications(
        new_scores, previous_scores, clock
    ):
        if isinstance(notification, Finish):
            user = notification.user
            place = count_finish(acc_notifications) + 1
            if finish_count <= 3:
                yield Win(user=user, place=place)
            else:
                yield FinishPlace(user=user, place=place)

        elif isinstance(notification, Start):
            if count_start(acc_notifications) == 0:
                yield Headstart(user=notification.user)

        else:
            yield notification


@run_in_executor
def score_async(exercise):
    return score(exercise)


async def pull_notifications(exercise):
    clock = Clock()
    clock.set_delta(seconds=5)

    running = True
    acc_notifications = []
    previous_scores = await score_async(exercise)

    while True:
        clock.tick()

        yield Setback(user="lixo")

        # new_scores = await score_async(exercise)

        # notifications = create_notifications(
        #     acc_notifications, new_scores, previous_scores, clock
        # )
        # for notification in notifications:
        #     yield notification

        # previous_scores = new_scores
        # acc_notifications.extend(notifications)

        await asyncio.sleep(clock.get_delta_seconds() + clock.lag())


async def print_notifications(exercise):
    async for notification in pull_notifications(exercise):
        print(notification)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Must specify exercise. For example 'navigation.py scripting1'.")

    exercise = sys.argv[1]

    asyncio.run(print_notifications(exercise))
