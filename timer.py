import time as t


class Timer:
    startTime = 0.0
    elapsed = 0.0

    def __init__(self):
        self.startTime = 0.0
        self.elapsed = 0.0

    def start_timer(self):
        """get starting time"""
        self.startTime = t.monotonic()

    def current_time(self):
        self.elapsed = (t.monotonic() - self.startTime)
        return self.elapsed

    def reset(self):
        self.startTime = 0.0
        self.elapsed = 0.0
        self.start_timer()
