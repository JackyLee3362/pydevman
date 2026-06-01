import time

from pydevman.decorator.common import run_once, timer, while_loop


def test_timer():
    pass

    @timer
    def my_func():
        # todo
        pass


def test_while_once():
    pass

    @while_loop
    def my_func():
        # todo
        pass


def test_run_once():
    @run_once
    def my_func(foo, bar):
        return foo + bar

    action = my_func(1, 2)
    assert action == 3
    action = my_func(3, 4)
    assert action is None
