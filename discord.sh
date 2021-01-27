#!/bin/bash

docker-compose run -d -w /leaderboard gago python3 discord_bot.py "$@"
