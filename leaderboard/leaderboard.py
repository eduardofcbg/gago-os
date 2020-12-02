from time import sleep
from operator import itemgetter

from dashing import VSplit, HSplit, HGauge

from users import get_users
from score import get_score

def chunks(l, n):
  for i in range(n):
      yield l[i::n]

def create_ui(scores):
  sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)

  gauges = [
    HGauge(val=score, title=name, border_color=5)
    for name, score in sorted_scores
  ]

  max_height = 20
  number_columns = int(len(gauges) / max_height) + 1

  columns = (
    VSplit(*chunk)
    for chunk in chunks(gauges, number_columns)
  )

  return HSplit(*columns)


if __name__ == '__main__':    
  while True:
    sleep(1)
    
    scores = {}
    for user in get_users():
      scores[user] = get_score(user)

    ui = create_ui(scores)
    ui.display()
