import asyncio
import io
import os
from dataclasses import dataclass

import discord
from discord.ext.commands import Bot, Group, Command

from bot.session import Chart
from bot.session_manager import SessionManager
from chart import get_scores as get_chart_scores, convert_svg_png
from render.chart import SVGChartEnv as ChartRenderEnv
from render.discrd import DiscordEnv as DiscordRenderEnv, DiscordTextMessage
from users import get_users as get_os_users

users = get_os_users()
session_manager = SessionManager(users)


@dataclass
class SubcommandNotFound:
    subcommand: str


async def create_chart_file(session, exercise):
    chart_render_env = ChartRenderEnv(session)

    scores = await get_chart_scores(session.registered_users, exercise)
    svg_text = chart_render_env.render(scores=scores)
    png_bytes = convert_svg_png(svg_text)

    return discord.File(io.BytesIO(png_bytes), filename="chart.png")


async def format_message(notification, session=None):
    if isinstance(notification, Chart):
        return await create_chart_file(session, notification.exercise)

    else:
        discord_render_env = DiscordRenderEnv(session)
        return DiscordTextMessage(discord_render_env, notification)


async def gago(ctx, subcommand):
    message = await format_message(SubcommandNotFound(subcommand))
    await ctx.reply(message)


async def push_notifications(channel_id, exercise):
    session = session_manager.get_session(channel_id)

    async for notification in session.start(exercise):
        channel = bot.get_channel(channel_id)
        message = await format_message(notification, session)

        if isinstance(message, discord.File):
            await channel.send(file=message)
        else:
            await channel.send(message)


async def start(ctx, exercise=None):
    channel_id = ctx.channel.id
    asyncio.create_task(push_notifications(channel_id, exercise))


async def stop(ctx):
    channel_id = ctx.channel.id
    session = session_manager.get_session(channel_id)

    notification = await session.stop()
    message = await format_message(notification, session)

    await ctx.reply(message)


async def periodic(ctx):
    channel_id = ctx.channel.id
    session = session_manager.get_session(channel_id)

    notification = session.toggle_periodic()
    message = await format_message(notification, session)

    await ctx.reply(message)


async def set_user(ctx, user=None):
    member = ctx.message.author
    channel_id = ctx.channel.id
    session = session_manager.get_session(channel_id)

    notification = session.register(user, member)
    message = await format_message(notification, session)

    await ctx.reply(message)


async def show_users(ctx):
    async with ctx.typing():
        members = ctx.guild.members
        channel_id = ctx.channel.id
        session = session_manager.get_session(channel_id)

        notification = session.get_users_status(members)
        message = await format_message(notification, session)

        await ctx.reply(message)


async def chart(ctx, exercise=None):
    channel_id = ctx.channel.id
    session = session_manager.get_session(channel_id)

    notification = session.chart(exercise)
    message = await format_message(notification, session)

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
group.add_command(Command(periodic, checks=[is_admin]))
group.add_command(Command(set_user, name="user", aliases=("setuser",)))
group.add_command(Command(show_users, name="users"))
group.add_command(Command(chart, aliases=("scores", "leaderboard")))

bot.add_command(group)

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    TOKEN = os.environ["DISCORD_BOT_TOKEN"]

    bot.run(TOKEN)
