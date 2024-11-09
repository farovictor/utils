# -*- coding: utf-8 -*-
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from typing import Callable
from typing import List

from core.logger.log import get_logger


class ProcessRunner:

    logger = get_logger(__name__)

    def __init__(
        self,
        num_workers: int,
        callables: Callable | List[Callable],
        lop_kwargs: List,
        *args,
        **kwargs
    ):
        self.nw = num_workers
        self.lop_callables = callables
        self.lop_kwargs = lop_kwargs
        self.results = []

    def execute(self):
        with Pool(processes=self.nw) as pool:
            if isinstance(self.lop_callables, List):
                self.logger.debug("Multible callabes passed.")
                results: List[AsyncResult] = [
                    pool.apply_async(func=fn, kwds=kwargs)
                    for fn, kwargs in zip(self.lop_callables, self.lop_kwargs)
                ]
                pool.close()
                pool.join()
            else:
                results = pool.map(self.lop_callables, self.lop_kwargs)

            self._collect(results)

    def __enter__(self):
        self.execute()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def _collect(self, results: List[AsyncResult]) -> List:
        self.results = [result.get() for result in results]

    @property
    def results(self) -> List:
        return self._results

    @results.setter
    def results(self, values: List[AsyncResult]):
        self._results = values