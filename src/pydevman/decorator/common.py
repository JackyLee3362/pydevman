import time
from functools import wraps


# 计时器
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(
            "Function {} has running for {:.2} seconds.".format(
                func.__name__, end - start
            )
        )

    return wrapper


# 设定超时时间
def while_loop(func, timeout=3):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        while time.time() - start < timeout:
            func(*args, **kwargs)

    return wrapper


# 打印参数
def args_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Arguments passed to the function:")
        print("Positional arguments:", args)
        print("Keyword arguments:", kwargs)
        func(*args, **kwargs)

    return wrapper


def run_once(f):
    """Run a function only once, no matter how many times it has been called.

    Examples:
        @run_once
        def my_function(foo, bar):
            return foo + bar

        while 1:
            my_function()

    Examples:
        def my_function(foo, bar):
            return foo + bar

        action = run_once(my_function)
        while 1:
            action()
    """

    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper
