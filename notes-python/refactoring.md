# Refactoring Python code

So, I decided to share a few techniques and tools I use to refactor Python code. Most of them are Python-specific, so you won't find them on resources like [refactoring.guru](https://refactoring.guru/).

This is the code we will refactor:

```python
import math
import sys
import httpx

deltas = []
bad_response = None
for _ in range(10):
    response = httpx.get('http://httpbin.org/status/200')
    if response.status_code != 200:
        bad_response = response
        break
    deltas.append(response.elapsed.microseconds)

if bad_response is not None:
    print(bad_response.status_code, bad_response.reason_phrase)
    sys.exit(1)

mean = sum(deltas) / len(deltas)
deviations = [mean - d for d in deltas]
variance = sum(d ** 2 for d in deviations) / len(deviations)
stddev = math.sqrt(variance)
print('mean:', mean)
print('std dev:', stddev)
```

It's a small script that already quite clean and works. It makes 10 requests to the URL and measures mean and standard deviation of elapsed time. This is how you can run it:

```bash
$ python3.9 speed_test.py
mean: 98965.0
std dev: 2108.0
```

If you just need it once for personal needs, it is already good enough. However, in this article we will turn this script into a proper CLI with the focus on making it easy to maintain in a big project. That means, the code will be longer and more "enterprizey" but at the same time much friendlier at the big scale.

Also, an important thing to note is that this code is just a small example. It could be even shorter using [statistics](https://docs.python.org/3/library/statistics.html). My goal was to select a minimal example that is enough for illusration but won't make the article too long. So, some changes here that make our example longer, will make the real world code shorter.

## Make it testable

First of all, we want this script to be testeable. Yes, you already can call it from tests using [subprocess](https://docs.python.org/3/library/subprocess.html), why not. However, such a test will be hard to write, hard to debug, slow to run, nearly impossible to calculate coverage. So, let's take all this code and do minimal changes to make it easy to test without any system calls, monkey patching, mocks, and so on.

1. Convert the main logic into a function to make it possible to call it from tests.
1. Pass parameters like URL as function arguments to let it to be re-defined from tests.
1. Pass the stream where we want to write the data as argument to avoid messing with stdout in tests.
1. Avoid `sys.exit` in the function, return the exit code instead.
1. Call the function under `if __name__ == '__main__'` so the script can be imported as a module.

This is what we get:

```python
import math
import sys
from typing import TextIO
import httpx


# Annotate types, it's already good and we'll need it later anyway
def speed_test(url: str, count: int, stream: TextIO) -> int:
    deltas = []
    bad_response = None
    # here we use the func arguments
    for _ in range(count):
        response = httpx.get(url)
        if response.status_code != 200:
            bad_response = response
            break
        deltas.append(response.elapsed.microseconds)

    if bad_response is not None:
        # pass `file=stream` into `print`
        print(bad_response.status_code, bad_response.reason_phrase, file=stream)
        # return the status code instead of `sys.exit`
        return 1

    mean = sum(deltas) / len(deltas)
    deviations = [mean - d for d in deltas]
    variance = sum(d ** 2 for d in deviations) / len(deviations)
    stddev = math.sqrt(variance)
    print('mean:', mean, file=stream)
    print('std dev:', stddev, file=stream)
    return 0

if __name__ == '__main__':
    sys.exit(speed_test(
        url='http://httpbin.org/status/200',
        count=10,
        stream=sys.stdout,
    ))
```

## Make it configureable

We have a few hardcoded values that we want to change sometimes. Namely, the website URL and requests' count. While it is fine for a quick small script, it is not so good if more people are going to use it more often than once a month. So, let's make these parameters configurable through CLI.

1. Use [argparse](https://docs.python.org/3/library/argparse.html), parse the CLI arguments, and pass them into the function.
1. Make the code that parses arguments also a function, so we are able to test it as well.

```python
from argparse import ArgumentParser
from typing import Sequence

...

def entrypoint(argv: Sequence[str]) -> int:
    parser = ArgumentParser()
    parser.add_argument('--url', default='http://httpbin.org/status/200')
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args(argv)
    return speed_test(
        url=args.url,
        count=args.count,
        stream=sys.stdout,
    )

if __name__ == '__main__':
    sys.exit(entrypoint(sys.argv[1:]))
```

## Make it extendeable

+ Let's use [attrs](http://attrs.org/) for parameters to make adding new params simpler and avoid overbloated function signatures.
+ Move the logic into `__call__` of this class.
+ Introduce helper methods to abstract away the logic from how we use it.

```python
import math
import sys
from argparse import ArgumentParser
from typing import TextIO, Sequence

import attr
import httpx


@attr.s(auto_attribs=True)
class SpeedTestCommand:
    url: str
    count: int
    stream: TextIO

    def _print(self, *args):
        print(*args, file=self.stream)

    def __call__(self) -> int:
        deltas = []
        bad_response = None
        for _ in range(self.count):
            response = httpx.get(self.url)
            if response.status_code != 200:
                bad_response = response
                break
            deltas.append(response.elapsed.microseconds)

        if bad_response is not None:
            self._print(bad_response.status_code, bad_response.reason_phrase)
            return 1

        mean = sum(deltas) / len(deltas)
        deviations = [mean - d for d in deltas]
        variance = sum(d ** 2 for d in deviations) / len(deviations)
        stddev = math.sqrt(variance)
        self._print('mean:', mean)
        self._print('std dev:', stddev)
        return 0


def entrypoint(argv: Sequence[str]) -> int:
    parser = ArgumentParser()
    parser.add_argument('--url', default='http://httpbin.org/status/200')
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args(argv)
    command = SpeedTestCommand(
        url=args.url,
        count=args.count,
        stream=sys.stdout,
    )
    return command()


if __name__ == '__main__':
    sys.exit(entrypoint(sys.argv[1:]))
```

## Make it declarative


```python
import math
import sys
from argparse import ArgumentParser
from datetime import timedelta
from typing import TextIO, Sequence, Tuple

import attr
import httpx
from cached_property import cached_property


@attr.s(auto_attribs=True)
class SpeedTestCommand:
    url: str
    count: int
    stream: TextIO

    _bad_response: httpx.Response = None

    def _print(self, *args):
        print(*args, file=self.stream)

    @cached_property
    def deltas(self) -> Tuple[timedelta, ...]:
        deltas = []
        for _ in range(self.count):
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

    def __call__(self) -> int:
        if self.failure:
            self._print(self.failure)
            return 1

        self._print('mean:', self.mean)
        self._print('std dev:', self.stddev)
        return 0


def entrypoint(argv: Sequence[str]) -> int:
    parser = ArgumentParser()
    parser.add_argument('--url', default='http://httpbin.org/status/200')
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args(argv)
    command = SpeedTestCommand(
        url=args.url,
        count=args.count,
        stream=sys.stdout,
    )
    return command()


if __name__ == '__main__':
    sys.exit(entrypoint(sys.argv[1:]))
```

## Make it maintaineable

1. Introduce base class for the command, move helper methods here.
1. Use python-fire to deduplicate defaults and autogenerate CLI.

```python
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
    count: int = 10

    _bad_response: httpx.Response = None
    ...

    def _do(self) -> int:
        if self.failure:
            self._print(self.failure)
            return 1

        self._print('mean:', self.mean)
        self._print('std dev:', self.stddev)

    def __call__(self) -> NoReturn:
        sys.exit(self._do())


def entrypoint(argv: Sequence[str]) -> int:
    try:
        Fire(SpeedTestCommand, command=argv)
    except SystemExit as exc:
        return exc.code


if __name__ == '__main__':
    sys.exit(entrypoint(sys.argv[1:]))
```

## Make it scallable

```python
import logging

...

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
```


## Result

```python
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
```
