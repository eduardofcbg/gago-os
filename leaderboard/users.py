from functools import lru_cache


@lru_cache(maxsize=None)
def get_users():
    with open("/config/users.txt") as users_file:
        lines = [line.strip() for line in users_file.read().splitlines()]
        return [line for line in lines if line]
