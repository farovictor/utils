# -*- coding: utf-8 -*-
from concurrent.futures import as_completed
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from typing import List

from core.logger.log import get_logger
from core.workers.base import Runner


class ThreadRunner(Runner):

    logger = get_logger(__name__)

    def __init__(
        self, num_workers: int, callables: Callable | List[Callable], op_kwargs: List
    ):
        self.nw = num_workers
        self.callables = callables
        self.op_kwargs = op_kwargs

    def execute(self):
        with ThreadPoolExecutor(max_workers=self.nw) as pool:
            tasks = []
            if isinstance(self.callables, List):
                self.logger.debug("Multible callabes passed.")
                tasks: List[Future] = [
                    pool.submit(fn, **kwargs)
                    for fn, kwargs in zip(self.callables, self.op_kwargs)
                ]

            else:
                tasks = pool.map(self.callables, self.op_kwargs)

            if as_completed(tasks):
                self._collect(tasks)

    def _collect(self, tasks: List[Future]) -> List:
        self.results = []
        for task in tasks:
            if isinstance(task, Future):
                task = task.result()
            self.results.append(task)
