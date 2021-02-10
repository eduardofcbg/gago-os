import asyncio

from score.scripts.remote import run_script

script_path = "/leaderboard/score/exercises/http_server/completed_log.sh"
max_completed = 11


async def score(user):
    completed_log = await run_script(user, script_path)
    completed = completed_log.splitlines()
    number_completed = sum(1 for task in completed if task.strip())

    return int(number_completed / max_completed * 100)


asyncio.run(score("ramane"))
