#!/usr/bin/env python

import csv
import sys
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

reader = csv.reader(sys.stdin, delimiter=",")
writer = csv.writer(sys.stdout, delimiter="|")

next(reader)

writer.writerow(["title", "platform", "user_score", "username"])

for row in reader:
    row_id, title, platform, user_score, comment, username = row
    writer.writerow([title, platform, user_score, username])
