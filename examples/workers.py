# -*- coding: utf-8 -*-
from logging import Logger

from core.logger.log import get_logger
from core.logger.log import logging_reformatting
from core.workers.concurrent import ThreadRunner
from core.workers.parallel import ProcessRunner


def figure(alice: bool, logger: Logger):
    if alice:
        logger.info("Alice is in wonderlands")
        return True
    logger.info("Is Alice awake?!")
    return False


def figure_p(alice: bool):
    # If you comment this, python will import from global scope
    # that is located in main process (parent), and will not create
    # multiple processes. ALWAYS ensure that your imports are made within process
    from core.logger.log import get_logger
    from core.logger.log import logging_reformatting

    logger = get_logger("process.handler")
    logging_reformatting()

    return figure(alice, logger)


def figure_c(alice: bool):
    logger = get_logger("thread.handler")
    logging_reformatting()

    return figure(alice, logger)


if __name__ == "__main__":
    with ProcessRunner(
        num_workers=2,
        callables=[figure_p, figure_p],
        op_kwargs=[{"alice": True}, {"alice": False}],
    ) as runner:
        assert runner.results == [True, False]

    with ThreadRunner(
        num_workers=2,
        callables=[figure_c, figure_c],
        op_kwargs=[{"alice": True}, {"alice": False}],
    ) as runner:
        assert runner.results == [True, False]
