from jinja2 import Environment, FileSystemLoader


class SVGChartEnv:
    def __init__(self):
        self.template_env = Environment(
            loader=FileSystemLoader("/config/discord/leaderboard"),
            auto_reload=False,
        )

    def render(self, **props):
        template = self.template_env.get_template("chart.svg")

        return template.render(props)
