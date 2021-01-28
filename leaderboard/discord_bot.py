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
CHART_FILE_PATH = "chart.png"


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


def mention(user):
    discord_member = user_discord_member.get(user)
    if discord_member:
        return discord_member.mention
    else:
        return user


@run_in_executor
def build_chart():
    def mention(user):
        discord_member = user_discord_member.get(user)
        if discord_member:
            return f"@{discord_member.name}"
        else:
            return user

    scores = [
        Score(user=mention(user), xp=score, place=place)
        for place, (user, score) in enumerate(
            sorted(get_score(exercise).items(), key=itemgetter(1)), 1
        )
    ]

    asc_scores = sorted(scores, key=attrgetter("xp"))
    dsc_scores = asc_scores[::-1]
    offset = 1 if len(asc_scores) % 2 == 0 else 0
    centered_scores = asc_scores[1::2] + dsc_scores[offset::2]

    svg_chart = format(Chart(scores=centered_scores))
    png_bytes = cairosvg.svg2png(bytestring=bytes(svg_chart, encoding="utf-8"))

    return png_bytes


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


async def start(ctx, _exercise):
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


async def chart(ctx):
    async with ctx.typing():
        png_bytes = await build_chart()

        picture = File(io.BytesIO(png_bytes), filename="chart.png")
        await ctx.reply(file=picture)


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
group.add_command(
    Command(
        chart,
        aliases=("scores", "showscores", "xp", "leaderboard"),
    )
)

bot.add_command(group)
bot.run(TOKEN)
