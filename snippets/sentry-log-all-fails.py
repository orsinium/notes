import atexit
import sys

from raven import Client


__all__ = ['sentry', 'register_sentry']


sentry = Client()


def log_last_error():
    info = sys.exc_info()
    if info[0] is not None:
        sentry.captureException(exc_info=info)


def register_sentry(dsn):
    """
    Pass here DSN and raven will send error in sentry if program fails.
    """
    sentry.set_dsn(dsn)
    atexit.register(log_last_error)
