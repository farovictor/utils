# -*- coding: utf-8 -*-
from core.workers.concurrent import ThreadRunner
from core.workers.parallel import ProcessRunner


def figure(alice: bool):
    from core.logger.log import get_logger

    logger = get_logger(__name__)
    if alice:
        logger.info("Alice is in wonderlands")
        return True
    logger.info("Is Alice awake?!")
    return False


def test_parallel_workers():
    with ProcessRunner(
        num_workers=1,
        callables=[figure, figure],
        op_kwargs=[{"alice": True}, {"alice": False}],
    ) as runner:
        assert runner.results == [True, False]


def test_concurrent_workers():
    with ThreadRunner(
        num_workers=2,
        callables=[figure, figure],
        op_kwargs=[{"alice": True}, {"alice": False}],
    ) as runner:
        assert runner.results == [True, False]
