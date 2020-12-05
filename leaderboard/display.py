import sys
from time import sleep
from operator import itemgetter

from dashing import VSplit, HSplit, HGauge

from users import get_users
from exercises.vim import get_score as get_score_vim
from exercises.navigation import get_score as get_score_navigation


def chunks(l, n):
    for i in range(n):
        yield l[i::n]


def create_ui(scores):
    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)

    gauges = [
        HGauge(val=score, title=name, border_color=5) for name, score in sorted_scores
    ]

    max_height = 20
    number_columns = int(len(gauges) / max_height) + 1

    columns = (VSplit(*chunk) for chunk in chunks(gauges, number_columns))

    return HSplit(*columns)


score_exercise = {"vim": get_score_vim, "navigation": get_score_navigation}

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(
            f"Leaderboard must be for an exercise. For example {tuple(score_exercise)} as first argument."
        )

    exercise = sys.argv[1]
    score = score_exercise[exercise]

    while True:
        sleep(1)

        scores = {user: score(user) for user in get_users()}

        ui = create_ui(scores)
        ui.display()
