
# Таймеры общего назначения

class RegularTimer:
    """Таймер регулярного повторения."""

    def __init__(self, handler, timeout):
        self.handler = handler
        self.timeout = timeout
        self.counter = 0

    def update(self, delta, args=()):
        if self.counter >= self.timeout:
            self.counter = 0
            self.handler(*args)
        else: self.counter += delta


class CountdownTimer:
    """Таймер обратного отсчёта."""

    def __init__(self, handler, timeout):
        self.handler = handler
        self.counter = timeout

    def update(self, delta, args=()):
        if self.counter > 0:
            self.handler(*args)
            self.counter -= delta

    def restart(self, new_timeout):
        self.counter = new_timeout
