from heapq import merge
import random

from python_profiling.multi_timer import MultiTimer
from python_profiling.profile_decorator import profile_function


def quick_sort(arr):
    """n lg n sort"""
    less = []
    pivot_list = []
    more = []

    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    for i in arr:
        if i < pivot:
            less.append(i)
        elif i > pivot:
            more.append(i)
        else:
            pivot_list.append(i)

    less = quick_sort(less)
    more = quick_sort(more)
    return less + pivot_list + more


def merge_sort(arr):
    """n lg n sort"""
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))


def heap_sort(arr):
    """n lg n sort"""
    arr_copy = arr[:]
    for start in range((len(arr_copy) - 2) // 2, -1, -1):
        siftdown(arr_copy, start, len(arr_copy) - 1)

    for end in range(len(arr_copy) - 1, 0, -1):
        arr_copy[end], arr_copy[0] = arr_copy[0], arr_copy[end]
        siftdown(arr_copy, 0, end - 1)
    return arr_copy


def siftdown(lst, start, end):
    root = start
    while True:
        child = root * 2 + 1
        if child > end: break
        if child + 1 <= end and lst[child] < lst[child + 1]:
            child += 1
        if lst[root] < lst[child]:
            lst[root], lst[child] = lst[child], lst[root]
            root = child
        else:
            break


def shell_sort(arr):
    """n lg^2 n sort"""
    arr_copy = arr[:]  # Sorts in place; make a duplicate.
    inc = len(arr_copy) // 2
    while inc:
        for i, el in enumerate(arr_copy[inc:], inc):
            while i >= inc and arr_copy[i - inc] > el:
                arr_copy[i] = arr_copy[i - inc]
                i -= inc
            arr_copy[i] = el
        inc = 1 if inc == 2 else inc * 5 // 11
    return arr_copy


def bubble_sort(arr):
    """n^2 Sort"""
    arr_copy = arr[:]  # Sorts in place
    changed = True
    while changed:
        changed = False
        for i in range(len(arr_copy) - 1):
            if arr_copy[i] > arr_copy[i + 1]:
                arr_copy[i], arr_copy[i + 1] = arr_copy[i + 1], arr_copy[i]
                changed = True
    return arr_copy


def run_one_sort(mt, sort_function, original_data, scrambled_data):
    sort_name = sort_function.__name__
    mt.record(sort_name)
    sorted_data = sort_function(scrambled_data)
    assert sorted_data == original_data


@profile_function()
def main():
    array_size = 15_000

    mt = MultiTimer()
    mt.start()

    mt.record("initialize")
    original_data = list(range(array_size))
    scrambled_data = original_data[:]
    random.shuffle(scrambled_data)

    run_one_sort(mt, quick_sort, original_data, scrambled_data)
    run_one_sort(mt, merge_sort, original_data, scrambled_data)
    run_one_sort(mt, heap_sort, original_data, scrambled_data)
    run_one_sort(mt, shell_sort, original_data, scrambled_data)
    if array_size <= 2_500:
        run_one_sort(mt, bubble_sort, original_data, scrambled_data)
    print(mt.report())


main()
