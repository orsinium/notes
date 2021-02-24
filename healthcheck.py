import logging
import math
import sys
from datetime import timedelta
from typing import TextIO, Sequence, Tuple, NoReturn

import attr
import httpx
from cached_property import cached_property
from fire import Fire


@attr.s(auto_attribs=True, kw_only=True)
class BaseCommand:
    stream: TextIO = sys.stdout

    def _print(self, *args):
        print(*args, file=self.stream)


@attr.s(auto_attribs=True, kw_only=True)
class SpeedTestCommand(BaseCommand):
    url: str = 'http://httpbin.org/status/200'
    count: int = 2

    _bad_response: httpx.Response = None

    @cached_property
    def deltas(self) -> Tuple[timedelta, ...]:
        deltas = []
        for _ in range(2):
            response = httpx.get(self.url)
            if response.status_code != 200:
                self._bad_response = response
                break
            deltas.append(response.elapsed.microseconds)
        return deltas

    @cached_property
    def failure(self) -> str:
        if self._bad_response is None:
            return ''
        return '{code} {reason}'.format(
            code=self._bad_response.status_code,
            reason=self._bad_response.reason_phrase,
        )

    @cached_property
    def mean(self) -> float:
        return sum(self.deltas) / len(self.deltas)

    @cached_property
    def deviations(self) -> Tuple[float, ...]:
        return tuple(self.mean - d for d in self.deltas)

    @cached_property
    def variance(self) -> float:
        return sum(d ** 2 for d in self.deviations) / len(self.deviations)

    @cached_property
    def stddev(self) -> float:
        return math.sqrt(self.variance)

    def _do(self) -> int:
        if self.failure:
            self._print(self.failure)
            return 1

        self._print('mean:', self.mean)
        self._print('std dev:', self.stddev)

    def __call__(self) -> NoReturn:
        sys.exit(self._do())


@attr.s(auto_attribs=True)
class Commands:
    log_level: str = 'WARNING'

    _registry = dict(
        speed=SpeedTestCommand,
    )

    def __call__(self):
        logging.getLogger().setLevel(self.log_level)
        return self._registry


def entrypoint(argv: Sequence[str]) -> int:
    try:
        Fire(Commands, command=argv)
    except SystemExit as exc:
        return exc.code


if __name__ == "__main__":
    sys.exit(entrypoint(sys.argv[1:]))
