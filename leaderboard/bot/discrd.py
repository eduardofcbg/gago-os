import io
import os
from dataclasses import dataclass

import discord
from discord.ext.commands import Bot, Group, Command

from bot.bot import Session as BotSession, Chart
from chart import get_scores as get_chart_scores, convert_svg_png
from render.discord import DiscordEnv as DiscordRenderEnv, DiscordTextMessage
from render.svg_chart import SVGChartEnv as ChartRenderEnv
from users import get_users as get_os_users
from utils import run_in_executor

users = get_os_users()
session = BotSession(users)

discord_render_env = DiscordRenderEnv(session)
chart_render_env = ChartRenderEnv()


@dataclass
class SubcommandNotFound:
    subcommand: str


def create_chart_file(exercise):
    scores = get_chart_scores(session.registered_users, exercise)
    svg_text = chart_render_env.render(scores=scores)
    png_bytes = convert_svg_png(svg_text)

    return discord.File(io.BytesIO(png_bytes), filename="chart.png")


@run_in_executor
def format_message(notification):
    if isinstance(notification, Chart):
        return create_chart_file(notification.exercise)

    else:
        return DiscordTextMessage(discord_render_env, notification)


async def gago(ctx, subcommand):
    message = await format_message(SubcommandNotFound(subcommand))
    await ctx.reply(message)


async def start(ctx, exercise=None):
    async for notification in session.start(exercise):
        message = await format_message(notification)

        await ctx.send(message)


async def stop(ctx):
    notification = await session.stop()
    message = await format_message(notification)

    await ctx.reply(message)


async def set_user(ctx, user=None):
    member = ctx.message.author
    notification = session.register(user, member)
    message = await format_message(notification)

    await ctx.reply(message)


async def show_users(ctx):
    async with ctx.typing():
        members = ctx.guild.members
        notification = session.get_users_status(members)
        message = await format_message(notification)

        await ctx.reply(message)


async def chart(ctx, exercise=None):
    notification = session.chart(exercise)
    message = await format_message(notification)

    if isinstance(message, discord.File):
        await ctx.reply(file=message)
    else:
        await ctx.reply(message)


intents = discord.Intents.default()
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
group.add_command(Command(show_users, name="users"))
group.add_command(Command(chart, aliases=("scores", "leaderboard")))

bot.add_command(group)

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    TOKEN = os.environ["DISCORD_BOT_TOKEN"]

    bot.run(TOKEN)
