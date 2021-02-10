from datetime import datetime, timedelta


class Clock:
    def __init__(self):
        self.current_tick = 0
        self.start_time = None
        self.delta = timedelta(seconds=1)

    def set_tick(self, tick):
        self.current_tick = tick

    def set_delta(self, **delta_args):
        self.delta = timedelta(**delta_args)

    def get_delta_seconds(self):
        return self.delta.total_seconds()

    def start(self):
        self.start_time = datetime.now()

    def tick(self, ticks=1):
        if not self.start_time:
            self.start()

        self.current_tick += ticks

    def lag(self):
        elapsed_goal = self.elapsed()
        elapsed = datetime.now() - self.start_time

        return (elapsed_goal - elapsed).total_seconds()

    def elapsed(self):
        return self.current_tick * self.delta

    def elapsed_seconds(self):
        return self.elapsed().total_seconds()

    def elapsed_minutes(self):
        return self.elapsed_seconds() / 60

    def elapsed_hours(self):
        return self.elapsed_minutes() / 60

    def tick_for(self, **delta_args):
        return int(timedelta(**delta_args) / self.delta)

    def is_multiple_of(self, **delta_args):
        tick_at_delta = self.tick_for(**delta_args)

        return (
            self.current_tick != 0
            and tick_at_delta != 0
            and self.current_tick % tick_at_delta == 0
        )

    def sleep_time(self):
        return self.get_delta_seconds() + self.lag()
