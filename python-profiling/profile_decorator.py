import functools
import io
import pstats
from cProfile import Profile
from datetime import datetime


def profile_function(print_report=False,
                     save_report=True,
                     file_name=f"profile-stats.{datetime.now().isoformat()}"):
    pr = Profile()

    def report():
        if print_report:
            sio = io.StringIO()
            ps = pstats.Stats(pr, stream=sio).strip_dirs().sort_stats('cumulative')
            ps.print_stats()
            print(sio.getvalue())
        if save_report:
            pr.dump_stats(file_name)

    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            pr.enable()  # Start data collection
            value = func(*args, **kwargs)
            pr.disable()  # Stop data collection
            report()
            return value

        return inner_wrapper

    return outer_wrapper


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


    @profile_function(file_name="flub-zub.dat")
    def fib_to_file(n: int) -> tuple[int, ...]:
        return dumb_fibonacci(n), memoized_fibonacci(n)


    @profile_function(print_report=True, save_report=False)
    def fib_to_screen(n: int) -> tuple[int, ...]:
        return dumb_fibonacci(n), memoized_fibonacci(n)


    print(fib_to_file(32))
    print(fib_to_screen(32))
