import sys
from time import sleep
from functools import reduce

from utils import one
from exercises.score import score
from clock import Clock


def merge_scores(accumulated_scores, scores):
    return {user: [*accumulated_scores[user], scores[user]] for user in scores}


def get_score_event(previous_score, score):
    def finish():
        return previous_score < 100 and score == 100

    def setback():
        return score < previous_score

    def jump():
        return score > previous_score

    def start():
        return previous_score == 0 and score > 0 and score != 100

    for event in [finish, setback, jump, start]:
        if event():
            return event.__name__
    else:
        return None


def get_events(previous_scores, scores):
    return {
        user: get_score_event(previous_scores[user], scores[user])
        for user in scores
    }


def get_event_history(accumulated_scores):
    def accumulate_events(acc, score_pair):
        event = get_score_event(*score_pair)

        return [*acc, event]

    return {
        user: reduce(accumulate_events, zip(scores, scores[1::]), [])
        for (user, scores) in accumulated_scores.items()
    }


def create_notifications(events_history, new_events, previous_scores, new_scores, clock):
    def winning_users():
        max_score = max(new_scores.values())
        return {
            user
            for (user, score) in new_scores.items()
            if score > 0 and score == max_score
        }

    def get_users_by_event(event):
        return {
            user
            for (user, user_event) in new_events.items()
            if event == user_event
        }

    def get_users_by_event_history(event):
        return {
            user
            for (user, user_events) in events_history.items()
            if event in user_events
        }

    user_notifications = {}

    if (
        clock.current_tick != 0
        and clock.current_tick % clock.tick_for(minutes=20) == 0
    ):
        for user in winning_users():
            user_notifications[user] = "winning"

    for (user, score) in new_scores:
        last_previous = previous_scores[user][-1]

        if score < last_previous:
            user_notifications[user] = "setback"

        if last_previous < 100 and score == 100:
            user_notifications[user] = "finish"

    # for user in get_users_by_event("setback"):
    #     user_notifications[user] = "setback"

    if not get_users_by_event_history("start"):
        for user in get_users_by_event("start"):
            user_notifications[user] = "start"

    previous_finish_count = len(get_users_by_event_history("finish"))
    finish_place = previous_finish_count + 1

    for user in get_users_by_event("finish"):
        user_notification[user] = "win" if finish_place < 3 else "finish"

    return user_notifications


def notify(exercise):
    clock = Clock()
    clock.set_delta(seconds=2)

    previous_scores = score(exercise)
    scores_history = {
        user: [score] for (user, score) in previous_scores.items()
    }

    while True:
        clock.tick()

        new_scores = score(exercise)

        events_history = get_event_history(scores_history)
        new_events = get_events(previous_scores, new_scores)
        yield create_notifications(
            events_history, new_events, previous_scores, new_scores, clock
        )

        previous_scores = new_scores
        scores_history = merge_scores(scores_history, new_scores)

        sleep(clock.get_delta_seconds() + clock.lag())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(
            f"Must specify exercise. For example 'navigation.py scripting1'."
        )

    execise = sys.argv[1]

    for notifications in notify(execise):
        from discord import notification_message

        for (user, event) in notifications.items():
            message = notification_message[event].format(user=user)
            print(message)
