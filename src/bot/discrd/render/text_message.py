from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader


class DiscordTextMessage:
    def __init__(self, env, notification):
        self.env = env
        self.notification = notification

    def __str__(self):
        return self.env.render(self.notification)


class DiscordEnv:
    def __init__(self, session):
        self.session = session
        self.template_env = Environment(
            loader=FileSystemLoader("/config/discord/src/messages"),
            auto_reload=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template_env.filters["mention"] = self._mention

    def _mention(self, user):
        discord_member = self.session.get_member(user)
        if discord_member:
            return discord_member.mention
        else:
            return user

    def render(self, message):
        template = self.template_env.get_template(type(message).__name__)
        props = asdict(message)

        return template.render(props)
