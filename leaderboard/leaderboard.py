from time import sleep
from operator import itemgetter

from dashing import VSplit, HGauge

def display(scores):
	sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)

	gauges = (
		HGauge(val=score, title=name, border_color=5)
		for name, score in sorted_scores
	)

	ui = VSplit(*gauges)
	ui.display()


if __name__ == '__main__':
	while True:
		sleep(1)
		# scores = score_users()

		import random
		scores = {
			'eduardo': random.choice([20, 30, 10, 50, 32]),
			'lixo': random.choice([20, 30, 10, 50, 32]),
		}

		display(scores)
