# built-in
import logging

from pythonjsonlogger.jsonlogger import RESERVED_ATTRS, merge_record_extra

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
WHITE = ''
RESET_SEQ = '\033[0m'

COLORS = {
    'DEBUG': BLUE,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': MAGENTA,
}


# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, colors=True, extras=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = colors
        self.extras = extras

    def format(self, record):
        # add color
        if self.colors and record.levelname in COLORS:
            start = COLORS[record.levelname]
            record.levelname = start + record.levelname + RESET_SEQ
            record.msg = WHITE + record.msg + RESET_SEQ

        # add extras
        if self.extras:
            extras = merge_record_extra(record=record, target=dict(), reserved=RESERVED_ATTRS)
            record.extras = ', '.join('{}={}'.format(k, v) for k, v in extras.items())
            if record.extras:
                record.extras = MAGENTA + '({})'.format(record.extras) + RESET_SEQ

        return super().format(record)
