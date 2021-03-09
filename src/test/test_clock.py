import time
import unittest

from clock import Clock


class TestClock(unittest.TestCase):
    def test_clock_default(self):
        clock = Clock()

        self.assertEqual(clock.elapsed_seconds(), 0)
        self.assertEqual(clock.get_delta_seconds(), 1)

        clock.tick()
        clock.tick(2)

        self.assertEqual(clock.elapsed_seconds(), 3)

    def test_clock_custom_delta(self):
        clock = Clock()
        clock.set_delta(days=1)

        self.assertEqual(clock.elapsed_seconds(), 0)
        self.assertEqual(clock.get_delta_seconds(), 24 * 60 * 60)

        clock.tick()

        self.assertEqual(clock.elapsed_hours(), 24)
        self.assertEqual(clock.elapsed_minutes(), 24 * 60)

    def test_clock_jump_ticks(self):
        clock = Clock()
        clock.set_delta(hours=1)

        self.assertEqual(clock.get_delta_seconds(), 60 * 60)

        clock.set_tick(5)
        clock.tick()

        self.assertEqual(clock.elapsed_hours(), 6)

        clock.set_tick(1)

        self.assertEqual(clock.elapsed_hours(), 1)

    def test_tick_for(self):
        clock = Clock()
        clock.set_delta(minutes=1)

        self.assertEqual(clock.tick_for(hours=1), 60)

    def test_lag_start(self):
        clock = Clock()
        clock.start()

        time.sleep(1)

        measured_lag = clock.lag()

        self.assertTrue(-1.1 <= measured_lag <= 1, measured_lag)

    def test_lag_tick(self):
        clock = Clock()
        clock.start()

        time.sleep(1)

        clock.tick()
        measured_lag = clock.lag()

        self.assertTrue(-0.1 <= measured_lag <= 0, measured_lag)
