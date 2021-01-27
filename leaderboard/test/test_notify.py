import unittest
from unittest.mock import patch

from notify import merge_scores, get_events, get_event_history


def mocked_get_score_event(previous_score, score):
    return "finish" if previous_score < 100 and score == 100 else None


class TestNotify(unittest.TestCase):
    def test_merge_scores(self):
        previous_acc_scores = {"user1": [1], "user2": [2]}
        scores = {"user1": 11, "user2": 22}
        expected_acc_scores = {"user1": [1, 11], "user2": [2, 22]}

        merged_scores = merge_scores(previous_acc_scores, scores)
        self.assertEqual(merged_scores, expected_acc_scores)

    def test_get_events(self):
        previous_score = {"user1": 50, "user2": 10, "user3": 100, "user4": 40}
        score = {"user1": 60, "user2": 100, "user3": 100, "user4": 10}
        expected_events = {
            "user1": "jump",
            "user2": "finish",
            "user3": None,
            "user4": "setback",
        }

        self.assertEqual(get_events(previous_score, score), expected_events)

    @patch("notify.get_score_event", side_effect=mocked_get_score_event)
    def test_get_event_history(self, get_score_event):
        acc_scores = {
            "user1": [0, 50, 100],
            "user2": [0, 20, 70],
        }
        expected_event_history = {
            "user1": [None, "finish"],
            "user2": [None, None],
        }

        self.assertEqual(get_event_history(acc_scores), expected_event_history)

    # # TODO: do not patch this
    # @patch("notify.get_score_events", side_effect=mocked_get_score_events)
    # def test_condense_events(self, get_score_events):
    #     clock = None

    #     acc_events1 = {
    #         "user1": ["finish", None, None],
    #         "user2": [None, "finish", None],
    #         "user3": [None, None, None],
    #         "user4": [None, None, None],
    #         "user5": [None, None, None],
    #     }
    #     events1 = {
    #         "user1": [None],
    #         "user2": [None],
    #         "user3": ["finish"],
    #         "user4": ["finish"],
    #         "user5": [None],
    #     }
    #     expected_condensed_events1 = {
    #         "win-draw": {"users": {"user3", "user4"}, "place": 3}
    #     }

    #     acc_events2 = {
    #         "user1": ["finish", None, None, None],
    #         "user2": [None, "finish", None, None],
    #         "user3": [None, None, None, "finish"],
    #         "user4": [None, None, None, "finish"],
    #         "user5": [None, None, None, None],
    #     }
    #     events2 = {
    #         "user1": [None],
    #         "user2": [None],
    #         "user3": [None],
    #         "user4": [None],
    #         "user5": ["finish"],
    #     }
    #     expected_condensed_events2 = {
    #         "finish": {"user": "user5", "place": 5},
    #     }

    #     self.assertEqual(
    #         condense_events(acc_events1, events1, clock),
    #         expected_condensed_events1,
    #     )
    #     self.assertEqual(
    #         condense_events(acc_events2, events2, clock),
    #         expected_condensed_events2,
    #     )
