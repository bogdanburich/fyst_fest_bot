import logging
import sentry_sdk

from config import ENVIRONMENT, SENTRY_DSN

FORMAT = '''[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(lineno)s]%(message)s'''  # noqa: E501


def get_logger(name):
    return logging.getLogger(name)


def init_logging():
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    if not ENVIRONMENT == 'DEV':
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=1.0
        )
