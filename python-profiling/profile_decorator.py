import functools
import logging
from cProfile import Profile
from datetime import datetime


def create_module_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter(
        fmt='%(asctime)s %(filename)s:%(lineno)d (%(funcName)s) %(message)s',
        datefmt="[%Y-%m-%d %H:%M:%S]"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_module_logger():
    return logging.getLogger(__name__)


def profile_functions(func):
    pr = Profile()
    logger = get_module_logger()

    def before():
        pr.enable()  # Start data collection

    def after():
        pr.disable()  # Stop data collection
        # TODO: Make direct printing an option.
        # See https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
        # sio = io.StringIO()
        # ps = pstats.Stats(pr, stream=sio).strip_dirs().sort_stats('cumulative')
        # ps.print_stats()  # Print profile stats into StringIO object.
        # print(sio.getvalue())
        file_name = f"dump.stats.{datetime.now().isoformat()}"
        logger.info(f"Dumped {file_name}")
        pr.dump_stats(file_name)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        before()
        value = func(*args, **kwargs)
        after()
        return value

    return wrapper


if __name__ == '__main__':
    logger = get_module_logger()


    def dumb_fibonacci(n: int) -> int:
        if n < 2:
            return 1
        else:
            return dumb_fibonacci(n - 1) + dumb_fibonacci(n - 2)


    @functools.cache
    def memoized_fibonacci(n: int) -> int:
        if n < 2:
            return 1
        else:
            return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


    @profile_functions
    def call_fibonacci(n: int) -> tuple[int, ...]:
        return dumb_fibonacci(n), memoized_fibonacci(n)


    logger.info(call_fibonacci(32))
