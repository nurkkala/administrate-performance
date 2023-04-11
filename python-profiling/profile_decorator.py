import functools
import io
import pstats
from cProfile import Profile


def profile_functions(func):
    pr = Profile()

    def before():
        pr.enable()  # Start data collection

    def after():
        pr.disable()  # Stop data collection
        sio = io.StringIO()
        ps = pstats.Stats(pr, stream=sio).strip_dirs().sort_stats('cumulative')
        ps.print_stats()  # Print profile stats into StringIO object.
        print(sio.getvalue())
        pr.dump_stats("dump.stats")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        before()
        value = func(*args, **kwargs)
        after()
        return value

    return wrapper


if __name__ == '__main__':
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


    print(call_fibonacci(32))
