#!/bin/bash

docker-compose run -w /leaderboard gago python3 discord_bot.py "$@"
