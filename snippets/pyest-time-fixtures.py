"""Some hooks and helpers to record how long it took to run each pytest fixture.
"""

import json
import time
from collections import defaultdict
from pathlib import Path

import pytest
from _pytest.fixtures import FixtureDef, SubRequest, FixtureRequest


TIMINGS = defaultdict(list)


# Record how long each fixture call takes
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: SubRequest):
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    TIMINGS[fixturedef.argname].append(end - start)


# Save the results when session is finished
def pytest_sessionfinish(session, exitstatus):
    res = sorted(TIMINGS.items(), key=lambda x: sum(x[-1]), reverse=True)
    res = json.dumps(dict(res), indent=2)
    Path("timings.json").write_text(res)

    res = {k: sum(v) for k, v in TIMINGS.items()}
    res = sorted(res.items(), key=lambda x: x[-1], reverse=True)
    res = json.dumps(dict(res), indent=2)
    Path("timings-cumulative.json").write_text(res)


# Trigger every fixture listed in the fixtures.txt file.
# You can use `pytest --fixtures` to list all available fixtures
# and then clean up the output with multicursor.
def test_trigger_all_fixtures(request: FixtureRequest):
    with open("fixtures.txt") as s:
        fixts = s.read().split()
    for fixt in fixts:
        try:
            request.getfixturevalue(fixt)
        except Exception:
            pass
