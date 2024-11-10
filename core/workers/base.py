# -*- coding: utf-8 -*-
import asyncio
from abc import ABC
from abc import abstractmethod
from typing import List


class Runner(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _collect(self, results: List) -> List:
        pass

    def __enter__(self):
        self.execute()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    @property
    def results(self) -> List:
        return self._results

    @results.setter
    def results(self, values: List):
        self._results = values

    def run_async_in_thread(async_func, *args, **kwargs):
        """Wrapper to run an async function in the event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(async_func(*args, **kwargs))
        finally:
            loop.close()
