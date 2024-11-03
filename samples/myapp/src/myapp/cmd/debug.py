import logging

from myapp.config import config
from myapp.database import database
from myapp.lib.context import context
from myapp.lib.logger import logger

LOG = logging.getLogger(__name__)


def main():
    logger.init()
    ctx = context.Context()

    db = database.DB()
    db.select()

    LOG.info("info", extra=ctx)
    LOG.debug("debug", extra=ctx)
