#!/usr/bin/env python3

import sys

file_name_left = sys.argv[1]
file_name_right = sys.argv[2]

with open(file_name_left, 'r') as left, open(file_name_right, 'r') as right:
	line_left = left.readline()
	line_right = right.readline()

	while line_left and line_right:
		if line_left == line_right:
			print(line_left, end='')
		else:
			break

		line_left = left.readline()
		line_right = right.readline()
