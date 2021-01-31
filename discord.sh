#!/bin/bash

./stopdiscord.sh
docker-compose run --name discordbot -w /leaderboard gago python3 discord_bot.py
