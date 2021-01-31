import unittest
from unittest.mock import patch, call

from datetime import datetime

from notify import pull_notifications, create_progress, create_periodic
from notify import Headstart, Win, FinishPlace, Setback, Winning
from clock import Clock


class TestNotify(unittest.IsolatedAsyncioTestCase):
    @patch("notify.create_progress", return_value=["some_notification"])
    @patch("notify.create_periodic", return_value=["periodic_notification"])
    @patch("notify.score", side_effect=[{"user1": 50}, {"user1": 100}])
    async def test_pull_notifications(
        self, score, create_periodic, create_progress
    ):
        notifications = pull_notifications(None)
        pulled = []

        while len(pulled) < 4:
            pulled.append(await notifications.__anext__())

        create_progress.assert_has_calls(
            [
                call({"user1": 50}, {"user1": 50}, []),
                call(
                    {"user1": 100},
                    {"user1": 50},
                    ["some_notification", "periodic_notification"],
                ),
            ]
        )

        self.assertEqual(
            pulled,
            [
                "some_notification",
                "periodic_notification",
                "some_notification",
                "periodic_notification",
            ],
        )

    @patch("notify.create_progress", return_value=["some_notification"])
    @patch("notify.create_periodic", return_value=[])
    @patch("notify.score", return_value={})
    async def test_pull_notifications_sleep_time(
        self, score, create_periodic, create_progress
    ):
        start_time = datetime.now()

        notifications = pull_notifications(None)
        pulled = []

        while len(pulled) < 3:
            pulled.append(await notifications.__anext__())

        measured_delay = (datetime.now() - start_time).total_seconds()

        self.assertTrue(10 <= measured_delay <= 10.1, measured_delay)

    def test_create_progress_headstart(self):
        acc_notifications = []
        previous_scores = {"user1": 0, "user2": 10}
        new_scores = {"user1": 10, "user2": 11}

        progress = create_progress(
            new_scores, previous_scores, acc_notifications
        )
        expected_progress = [Headstart(user="user1")]

        self.assertEqual(list(progress), expected_progress)

    def test_create_progress_headstart(self):
        acc_notifications = [Headstart(user="user2")]
        previous_scores = {"user1": 0, "user2": 10}
        new_scores = {"user1": 10, "user2": 11}

        progress = create_progress(
            new_scores, previous_scores, acc_notifications
        )
        expected_progress = []

        self.assertEqual(list(progress), expected_progress)

    def test_create_progress_win(self):
        acc_notifications = [Win(user="user3", place=1)]
        previous_scores = {
            "user1": 0,
            "user2": 90,
            "user3": 100,
        }
        new_scores = {
            "user1": 100,
            "user2": 100,
            "user3": 100,
        }

        progress = create_progress(
            new_scores, previous_scores, acc_notifications
        )
        expected_progress = [
            Win(user="user1", place=2),
            Win(user="user2", place=2),
        ]

        self.assertEqual(list(progress), expected_progress)

    def test_create_progress_finish(self):
        acc_notifications = [
            Win(user="user1", place=1),
            Win(user="user2", place=2),
            Win(user="user3", place=2),
            FinishPlace(user="user4", place=4),
        ]
        previous_scores = {
            "user1": 100,
            "user2": 100,
            "user3": 100,
            "user4": 100,
            "user5": 90,
        }
        new_scores = {
            "user1": 100,
            "user2": 100,
            "user3": 100,
            "user4": 100,
            "user5": 100,
        }

        progress = create_progress(
            new_scores, previous_scores, acc_notifications
        )
        expected_progress = [FinishPlace(user="user5", place=5)]

        self.assertEqual(list(progress), expected_progress)

    def test_create_progress_setback(self):
        acc_notifications = []
        previous_scores = {
            "user1": 50,
            "user2": 50,
            "user3": 50,
        }
        new_scores = {
            "user1": 40,
            "user2": 30,
            "user3": 70,
        }

        progress = create_progress(
            new_scores, previous_scores, acc_notifications
        )
        expected_progress = [Setback(user="user1"), Setback(user="user2")]

        self.assertEqual(list(progress), expected_progress)

    def test_create_periodic(self):
        new_scores = {"user1": 40, "user2": 50, "user3": 50, "user4": 10}
        clock = Clock()
        clock.set_delta(minutes=1)
        clock.tick(19)

        periodic = create_periodic(new_scores, clock)

        self.assertEqual(list(periodic), [])

        clock.tick(1)
        periodic = create_periodic(new_scores, clock)

        self.assertEqual(list(periodic), [Winning(users={"user2", "user3"})])
