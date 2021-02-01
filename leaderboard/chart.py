from dataclasses import dataclass
from operator import itemgetter
from typing import Any

import cairosvg

from exercises.score import score as get_score


@dataclass
class Score:
    user: Any
    xp: int
    place: int


def _center_scores(dsc_scores):
    asc_scores = dsc_scores[::-1]
    offset = 1 if len(asc_scores) % 2 == 0 else 0
    centered_scores = asc_scores[1::2] + dsc_scores[offset::2]

    return centered_scores


def get_scores(users, exercise):
    if len(users) == 0:
        raise ValueError("No users to score")

    dsc_scores = sorted(get_score(exercise).items(), key=itemgetter(1), reverse=True)
    dsc_placed_users = [
        Score(user=user, xp=score, place=place)
        for place, (user, score) in enumerate(dsc_scores, 1)
        if user in users
    ]

    return _center_scores(dsc_placed_users)


def convert_svg_png(svg_text):
    png_bytes = cairosvg.svg2png(bytestring=bytes(svg_text, encoding="utf-8"))

    return png_bytes
