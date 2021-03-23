from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader


class TextMessageRenderer:
    def __init__(self):
        self.template_env = Environment(
            loader=FileSystemLoader("/config/discord/leaderboard/messages"),
            auto_reload=False,
            enable_async=True,
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

    def render(self, session, message):
        self.session = session
        template = self.template_env.get_template(type(message).__name__)
        props = asdict(message)

        return template.render_async(props)
