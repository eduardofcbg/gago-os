import os
import io
from typing import List, Dict
from operator import attrgetter, itemgetter
from dataclasses import dataclass, asdict

import cairosvg
from jinja2 import Environment, FileSystemLoader
from discord.ext.commands import Bot, Group, Command
from discord import Intents, File

from utils import run_in_executor
from users import get_users as get_os_users
from exercises.score import score as get_score
from notify import pull_notifications
from exercises.score import is_valid_exercise


TOKEN = os.environ["DISCORD_BOT_TOKEN"]


@dataclass
class Go:
    pass


@dataclass
class Stop:
    exercise: str


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


@dataclass
class AlreadySetUser:
    user: str


@dataclass
class InvalidUser:
    user: str


@dataclass
class Chart:
    scores: List[int]


@dataclass
class Score:
    user: str
    xp: int
    place: int


user_discord_member = {}
notifications = None
exercise = None


def get_chart_scores(_exercise):
    dsc_scores = [
        Score(user=user, xp=score, place=place)
        for place, (user, score) in enumerate(
            sorted(
                get_score(_exercise).items(), key=itemgetter(1), reverse=True
            ),
            1,
        )
    ]
    asc_scores = dsc_scores[::-1]
    offset = 1 if len(asc_scores) % 2 == 0 else 0
    centered_scores = asc_scores[1::2] + dsc_scores[offset::2]

    return centered_scores


@run_in_executor
def build_chart(_exercise):
    centered_scores = get_chart_scores(_exercise)
    svg_chart = format(Chart(scores=centered_scores))
    png_bytes = cairosvg.svg2png(bytestring=bytes(svg_chart, encoding="utf-8"))

    return png_bytes


def mention(user):
    discord_member = user_discord_member.get(user)
    if discord_member:
        return discord_member.mention
    else:
        return user


template_env = Environment(
    loader=FileSystemLoader("/config/discord/leaderboard/messages"),
    auto_reload=True,
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


async def start(ctx, _exercise=None):
    global notifications
    global exercise

    if not is_valid_exercise(_exercise):
        await ctx.reply(format(InvalidExercise(_exercise)))

    elif not notifications:
        await ctx.reply(format(Go()))

        exercise = _exercise
        notifications = pull_notifications(exercise)

        async for notification in notifications:
            await ctx.send(format(notification))


async def stop(ctx):
    global notifications
    global exercise

    if notifications:
        await ctx.reply(format(Stop(exercise=exercise)))

        await notifications.aclose()
        notifications = None
        exercise = None


async def set_user(ctx, user=None):
    if user not in get_os_users():
        await ctx.reply(format(InvalidUser(user)))

    elif user in user_discord_member:
        await ctx.reply(format(AlreadySetUser(user)))

    else:
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
            user: member.mention for user, member in user_discord_member.items()
        }

        message = ShowUsers(
            user_discord_mention=user_discord_mention,
            users_not_member=sorted(users_not_member),
            members_not_user=members_not_user,
        )

        await ctx.reply(format(message))


async def chart(ctx, _exercise=None):
    global exercise

    chart_exercise = _exercise or exercise

    if not is_valid_exercise(chart_exercise):
        await ctx.reply(format(InvalidExercise(chart_exercise)))

    else:
        async with ctx.typing():
            png_bytes = await build_chart(chart_exercise)
            picture = File(io.BytesIO(png_bytes), filename="chart.png")

            await ctx.reply(file=picture)


intents = Intents.default()
intents.members = True
bot = Bot(intents=intents, command_prefix=("$", "!", "/"))

group = Group(gago, invoke_without_command=True)


def is_admin(ctx):
    channel = ctx.channel
    permissions = channel.permissions_for(ctx.author)
    return permissions.administrator


group.add_command(Command(start, checks=[is_admin]))
group.add_command(Command(stop, checks=[is_admin]))
group.add_command(Command(set_user, name="user", aliases=("setuser",)))
group.add_command(
    Command(
        show_users,
        name="users",
        aliases=("showusers",),
    )
)
group.add_command(
    Command(
        chart,
        name="chart",
        aliases=("scores", "showscores", "xp", "leaderboard"),
    )
)

bot.add_command(group)
bot.run(TOKEN)
