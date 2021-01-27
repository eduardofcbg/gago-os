import os
from typing import List, Dict
from dataclasses import dataclass, asdict
from functools import partial

from jinja2 import Environment, DictLoader, FileSystemLoader
from discord.ext.commands import Bot, Group, Command
from discord import Intents

from users import get_users as get_os_users
from notify import pull_notifications
from exercises.score import is_valid_exercise


TOKEN = os.environ["DISCORD_BOT_TOKEN"]


@dataclass
class Go:
    pass


@dataclass
class Stop:
    pass


@dataclass
class UserSet:
    user: str


@dataclass
class ShowUsers:
    user_discord_mention: Dict[str, str]
    users_not_member: List[str]
    members_not_user: List[str]


@dataclass
class SubcommandNotFound:
    subcommand: str


@dataclass
class InvalidExercise:
    exercise: str


user_discord_member = {}
notifications = None


def mention(user):
    discord_member = user_discord_member.get(user)
    if discord_member:
        return discord_member.mention
    else:
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


async def gago(ctx, subcommand):
    await ctx.reply(format(SubcommandNotFound(subcommand)))


async def start(ctx, exercise):
    global notifications

    if not is_valid_exercise(exercise):
        await ctx.reply(format(InvalidExercise(exercise)))

    elif not notifications:
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


async def set_user(ctx, user):
    discord_member = ctx.message.author
    user_discord_member[user] = discord_member

    message = UserSet(user=user)

    await ctx.reply(format(message))


async def show_users(ctx):
    async with ctx.typing():
        all_users = set(get_os_users())
        users_member = set(user_discord_member)
        users_not_member = all_users - users_member
        members_not_user = list(member.mention for member in ctx.guild.members)

        user_discord_mention = {
            user: member.mention for (user, member) in user_discord_member.items()
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

group = Group(gago, invoke_without_command=True)

group.add_command(Command(start))
group.add_command(Command(stop))
group.add_command(
    Command(
        set_user,
        name="user",
        aliases=("setuser",),
    )
)
group.add_command(
    Command(
        show_users,
        name="users",
        aliases=("showusers",),
    )
)

bot.add_command(group)
bot.run(TOKEN)
