from typing import List, Dict
from dataclasses import dataclass, asdict
from functools import partial

from jinja2 import Environment, DictLoader, FileSystemLoader
from discord.ext.commands import Bot, Command
from discord import Intents

from users import get_users as get_os_users
from notify import pull_notifications


@dataclass
class Go:
    pass


@dataclass
class Stop:
    pass


@dataclass
class UserSetup:
    user: str


@dataclass
class ShowUsers:
    user_discord_mention: Dict[str, str]
    users_not_member: List[str]
    members_not_user: List[str]


user_discord_member = {}
notifications = None


def mention(user):
    discord_member = user_discord_member.get(user)
    if discord_member:
        return discord_member.mention
    else:
        print(f"User {user} is not registered as member")
        return user


template_env = Environment(
    loader=FileSystemLoader("/config/discord/leaderboard/messages"),
    auto_reload=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
template_env.filters["mention"] = mention


def format(message):
    template = template_env.get_template(type(message).__name__)
    message = asdict(message)

    return template.render(message)


async def start(ctx, exercise):
    global notifications

    if notifications:
        print("Leaderboard already running")
    else:
        await ctx.reply(format(Go()))
        notifications = pull_notifications(exercise)

        for notification in notifications:
            await ctx.send(format(notification))


async def stop(ctx):
    global notifications

    if notifications:
        notifications.close()
        notifications = None
        await ctx.reply(format(Stop()))
    else:
        print("No leaderboard running")


async def setup_user(ctx, user):
    discord_member = ctx.message.author
    user_discord_member[user] = discord_member

    message = UserSetup(user=user)

    await ctx.reply(format(message))


async def show_users(ctx):
    async with ctx.typing():
        all_users = set(get_os_users())
        users_member = set(user_discord_member)
        users_not_member = all_users - users_member
        members_not_user = list(member.mention for member in ctx.guild.members)

        user_discord_mention = {
            user: member.mention
            for (user, member) in user_discord_member.items()
        }

        message = ShowUsers(
            user_discord_mention=user_discord_mention,
            users_not_member=sorted(users_not_member),
            members_not_user=members_not_user,
        )

        await ctx.reply(format(message))


intents = Intents.default()
intents.members = True
bot = Bot(intents=intents, command_prefix=("$", "!", "/"))

bot.add_command(
    Command(
        stop,
        name="stop-leaderboard",
        aliases=("leaderboard-stop",),
    )
)
bot.add_command(
    Command(
        start,
        name="leaderboard",
        aliases=("start-leaderboard", "leaderboard-start"),
    )
)
bot.add_command(
    Command(
        setup_user,
        name="leaderboard-user",
        aliases=("user-leaderboard",),
    )
)
bot.add_command(
    Command(
        show_users,
        name="leaderboard-users",
        aliases=("users-leaderboard",),
    )
)

token = "ODAzMjk4MTI4MDYwNDgxNTk2.YA7vrg.ZopTLhSNUNylq99aQeEIa-7r--c"
bot.run(token)
