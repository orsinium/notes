# built-in
import logging


class LevelFilter(logging.Filter):
    """Filter log by min or max severity level.
    """

    def __init__(self, low=logging.DEBUG, high=logging.CRITICAL):
        # Convert str level representation to level number.
        # Example: "DEBUG" -> 10
        if isinstance(low, str):
            low = getattr(logging, low)
        if isinstance(high, str):
            high = getattr(logging, high)

        self._low = low
        self._high = high
        super().__init__()

    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False
