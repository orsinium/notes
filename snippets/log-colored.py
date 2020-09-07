# built-in
import logging

from pythonjsonlogger.jsonlogger import RESERVED_ATTRS, merge_record_extra

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[1;{:d}m'
BOLD_SEQ = '\033[1m'

COLORS = {
    'DEBUG': BLUE,
    'INFO': GREEN,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': CYAN,
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
            start = COLOR_SEQ.format(COLORS[record.levelname])
            record.levelname = start + record.levelname + RESET_SEQ
            record.msg = COLOR_SEQ.format(WHITE) + record.msg + RESET_SEQ

        # add extras
        if self.extras:
            extras = merge_record_extra(record=record, target=dict(), reserved=RESERVED_ATTRS)
            record.extras = ', '.join('{}={}'.format(k, v) for k, v in extras.items())
            if record.extras:
                record.extras = COLOR_SEQ.format(MAGENTA) + '({})'.format(record.extras) + RESET_SEQ

        return super().format(record)
