# -*- coding: utf-8 -*-
from core.workers.parallel import ProcessRunner


def figure(alice: bool):
    from core.logger.log import get_logger

    logger = get_logger(__name__)
    if alice:
        logger.info("Alice is in wonderlands")
        return True
    logger.info("Alice is waken?!")
    return False


def test_parallel_workers():
    with ProcessRunner(
        num_workers=1,
        callables=[figure, figure],
        lop_kwargs=[{"alice": True}, {"alice": False}],
    ) as runner:
        assert runner.results == [True, False]
