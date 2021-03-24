import asyncio
import sys
from operator import itemgetter

from dashing import VSplit, HSplit, HGauge

from clock import Clock
from score.exercises.score import score


def chunks(l, n):
    for i in range(n):
        yield l[i::n]


def create_title(name, score):
    return f"{name} ({score}xp)"


def create_ui(scores):
    dsc_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)

    gauges = [
        HGauge(val=score, title=create_title(name, score), border_color=5, color=5)
        for name, score in dsc_scores
    ]

    max_height = 20
    number_columns = int(len(gauges) / max_height) + 1

    columns = (VSplit(*chunk) for chunk in chunks(gauges, number_columns))

    return HSplit(*columns)


async def refresh_leaderboard(exercise, users):
    clock = Clock()
    clock.set_delta(seconds=10)
    clock.start()

    while True:
        scores = await score(exercise, users)

        ui = create_ui(scores)
        ui.display()

        await asyncio.sleep(clock.sleep_time())
        clock.tick()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            f"Leaderboard must be for an exercise. For example 'display.py scripting'."
        )

    exercise = sys.argv[1]
    users = sys.argv[2::]

    asyncio.run(refresh_leaderboard(exercise, users or None))
