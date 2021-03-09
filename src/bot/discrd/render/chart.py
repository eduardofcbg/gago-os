from jinja2 import Environment, FileSystemLoader


class SVGChartEnv:
    def __init__(self, session):
        self.session = session
        self.template_env = Environment(
            loader=FileSystemLoader("/config/discord/src"),
            auto_reload=True,
        )
        self.template_env.filters["mention"] = self._mention
        self.template_env.filters["avatar_url"] = self._avatar_url

    def _mention(self, user):
        discord_member = self.session.get_member(user)
        if discord_member:
            return discord_member.display_name
        else:
            return user

    def _avatar_url(self, user):
        discord_member = self.session.get_member(user)
        if discord_member:
            return discord_member.avatar_url
        else:
            return None

    def render(self, **props):
        template = self.template_env.get_template("chart.svg")

        return template.render(props)
