import sys
from time import sleep
from functools import reduce

from utils import one
from exercises.score import score
from clock import Clock


def merge_scores(accumulated_scores, scores):
    return {user: [*accumulated_scores[user], scores[user]] for user in scores}


def get_score_events(previous_score, score):
    def finish():
        return previous_score < 100 and score == 100

    def setback():
        return score < previous_score

    def archive():
        return score > previous_score

    def start():
        return previous_score == 0 and score > 0 and score != 100

    validate_event = zip(
        ["finish", "setback", "archive", "start"], [finish, setback, archive, start]
    )
    matched_events = [
        event_name for (event_name, is_event) in validate_event if is_event()
    ]

    return matched_events if matched_events else [None]


def get_events(previous_scores, scores):
    return {
        user: get_score_events(previous_scores[user], scores[user]) for user in scores
    }


def get_event_history(accumulated_scores):
    def accumulate_events(acc, score_pair):
        events = get_score_events(*score_pair)

        return [*acc, *events]

    return {
        user: reduce(accumulate_events, zip(scores, scores[1::]), [])
        for (user, scores) in accumulated_scores.items()
    }


def condense_events(scores, events_history, new_events, clock):
    def get_users_matching(events, event):
        return {user for (user, events) in events.items() if event in events}

    def get_finished_users(events):
        return get_users_matching(events, "finish")

    def get_started_users(events):
        return get_users_matching(events, "start")

    def handle_finish_event():
        previous_finish_count = len(get_finished_users(events_history))
        finished_users = get_finished_users(new_events)

        finish_event = "win" if previous_finish_count < 3 else "finish"
        finish_place = previous_finish_count + 1

        if len(finished_users) > 1:
            return {
                f"{finish_event}-draw": {
                    "users": finished_users,
                    "place": finish_place,
                }
            }
        elif finished_users:
            return {
                finish_event: {
                    "user": one(finished_users),
                    "place": finish_place,
                }
            }

    def handle_start_event():
        started_users = get_started_users(events_history)
        new_started_users = get_started_users(new_events)
        if not started_users and new_started_users:
            return {"start": {"users": new_started_users}}

    def handle_setback_event():
        setback_users = get_users_matching(events_history, "setback")
        if setback_users:
            return {"setback": {"users": setback_users}}

    def do_every_20_minutes():
        if clock.tick_for(minutes=20) % clock.current_tick == 0:
            # TODO
            pass

    

    condensed_events = {}

    for events in [
        handle_finish_event(),
        handle_start_event(),
        handle_setback_event(),
        do_every_20_minutes(),
    ]:
        if events:
            condensed_events = {**condensed_events, **events}

    return condensed_events


if __name__ == "main":
    if len(sys.argv) != 2:
        sys.exit(f"Must specify exercise. For example 'navigation.py scripting1'.")

    execise = sys.argv[1]

    clock = Clock()
    clock.set_delta(seconds=1)

    scores_history = {}
    previous_scores = {}

    while True:
        scores = score(exercise)

        events_history = get_event_history(scores_history)
        new_events = get_events(previous_scores, scores)
        events = condense_events(scores, events_history, new_events, clock)

        previous_scores = scores
        scores_history = merge_scores(scores_history, scores)

        sleep(clock.get_delta_seconds())
        clock.tick()
