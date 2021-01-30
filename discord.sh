#!/bin/bash

docker-compose run -d --name discordbot -w /leaderboard gago python3 discord_bot.py
