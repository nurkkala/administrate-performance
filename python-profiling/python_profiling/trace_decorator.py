import functools
from datetime import datetime
from trace import Trace, CoverageResults


def trace_function(print_report=False,
                   save_report=True,
                   file_name=f"trace-stats.{datetime.now().isoformat()}"):
    tr = Trace(count=1,
               trace=1,
               countfuncs=1,
               countcallers=1,
               ignoremods=(),
               ignoredirs=(),
               infile=None,
               outfile=None,
               timing=True)

    def report(results: CoverageResults):
        results.write_results(show_missing=True, summary=True)

    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            value = tr.runfunc(func, *args, **kwargs)
            report(tr.results())
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


    @trace_function()
    def fib_to_file(n: int) -> tuple[int, ...]:
        return dumb_fibonacci(n), memoized_fibonacci(n)


    @trace_function(print_report=True, save_report=False)
    def fib_to_screen(n: int) -> tuple[int, ...]:
        return dumb_fibonacci(n), memoized_fibonacci(n)


    nth_fib_number = 5
    print(fib_to_file(nth_fib_number))
    print(fib_to_screen(nth_fib_number))
