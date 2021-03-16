#!/usr/bin/env python

import csv
import sys
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

reader = csv.reader(sys.stdin, delimiter=",")
writer = csv.writer(sys.stdout, delimiter="|")

next(reader)

writer.writerow(["title", "year", "publisher", "genre", "platform", "players"])

for row in reader:
    row_id, title, year, publisher, genre, platform, meta_score, user_score, players = row
    writer.writerow([title, year, publisher, genre, platform, players])
