import random
from time import sleep

import pytest

from python_profiling.multi_timer import MultiTimer, MTState


@pytest.fixture
def mt():
    return MultiTimer()


def test_init_state(mt):
    assert mt.state == MTState.READY
    assert len(mt.records) == 0


def test_start_state(mt):
    mt.start()
    assert mt.state == MTState.RUNNING
    assert len(mt.records) == 1
    assert '[START]' in mt.report()


def test_bogus_start_transitions(mt):
    mt.start()
    with pytest.raises(AssertionError):
        mt.start()

# def run_one_test(multi_timer: MultiTimer, prefix=""):
#     multi_timer.start()
#     for label in ['alpha', 'beta', 'gamma']:
#         nap_time = random.random() / 10.0
#         random_flags = random.randint(0, 8)
#         print(label, nap_time)
#         sleep(nap_time)
#         multi_timer.record(label, random_flags)
#     multi_timer.report(prefix)
#
#
# mt = MultiTimer()
# run_one_test(mt)
# mt.reset()
# run_one_test(mt, "CPU0")
