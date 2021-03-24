import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from chart import get_scores, Score
from score.exercises.score import is_valid_exercise
from notify import pull_notifications, Surpass, Winning, Win, FinishPlace, Periodic
from utils import cancel_gen


@dataclass
class InvalidUser:
    user: Any


@dataclass
class AlreadySetUser:
    user: Any


@dataclass
class AlreadySetMember:
    member: Any


@dataclass
class UserSet:
    user: Any


@dataclass
class ShowUsers:
    user_to_mention: Dict
    unregistered_users: List
    unregistered_mentions: List


@dataclass
class AlreadyRunning:
    pass


@dataclass
class Go:
    pass


@dataclass
class NotRunning:
    pass


@dataclass
class Stop:
    exercise: Any


@dataclass
class EnabledPeriodic:
    pass


@dataclass
class DisabledPeriodic:
    pass


@dataclass
class NoExercise:
    pass


@dataclass
class InvalidExercise:
    exercise: Any


@dataclass
class Chart:
    chart_scores: List[Score]


class Session:
    def __init__(self, users):
        self.users = set(users)
        self.user_to_member = {}
        self.notifications = None
        self.exercise = None
        self.send_periodic = True

    @property
    def running(self):
        return bool(self.notifications)

    @property
    def registered_users(self):
        return set(self.user_to_member)

    def _deregister(self, deregister_member):
        self.user_to_member = {
            user: member
            for user, member in self.user_to_member.items()
            if member != deregister_member
        }

    def _get_chart_scores(self, exercise):
        return get_scores(self.registered_users, exercise)

    def register(self, user, member):
        if user not in self.users:
            return InvalidUser(user=user)

        elif user in self.registered_users:
            return AlreadySetUser(user=user)

        else:
            self._deregister(member)
            self.user_to_member[user] = member
            return UserSet(user=user)

    def get_member(self, user):
        return self.user_to_member.get(user)

    def get_users_status(self, online_members):
        unregistered_users = sorted(self.users - self.registered_users)
        registered_members = set(self.user_to_member.values())
        unregistered_mentions = sorted(
            member.mention for member in set(online_members) - registered_members
        )
        user_to_mention = {
            user: member.mention for user, member in self.user_to_member.items()
        }

        return ShowUsers(
            user_to_mention=user_to_mention,
            unregistered_users=unregistered_users,
            unregistered_mentions=unregistered_mentions,
        )

    async def start(self, exercise):
        if self.running:
            yield AlreadyRunning()
        else:
            self.notifications = pull_notifications(exercise, self.registered_users)
            self.exercise = exercise

            yield Go()

            try:
                chart_scores = await self._get_chart_scores(self.exercise)
                yield Chart(chart_scores=chart_scores)
            except (IOError, OSError) as e:
                logging.exception(e)

            async for notification in self.notifications:
                if isinstance(notification, Periodic) and not self.send_periodic:
                    continue

                yield notification

                if isinstance(notification, (Surpass, Winning, Win, FinishPlace, Stop)):
                    try:
                        chart_scores = await self._get_chart_scores(self.exercise)
                        yield Chart(chart_scores=chart_scores)
                    except (IOError, OSError) as e:
                        logging.exception(e)

    async def stop(self):
        if not self.running:
            return NotRunning()

        await cancel_gen(self.notifications)

        message = Stop(exercise=self.exercise)

        self.notifications = None
        self.exercise = None

        return message

    def toggle_periodic(self):
        self.send_periodic = not self.send_periodic

        return EnabledPeriodic() if self.send_periodic else DisabledPeriodic()

    async def chart(self, exercise=None):
        chart_exercise = self.exercise or exercise

        if not chart_exercise:
            yield NoExercise()
        elif not is_valid_exercise(chart_exercise):
            yield InvalidExercise(exercise=chart_exercise)
        else:
            chart_scores = await self._get_chart_scores(chart_exercise)
            yield Chart(chart_scores=chart_scores)
