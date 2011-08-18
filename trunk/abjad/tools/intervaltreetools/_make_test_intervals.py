from abjad.tools.intervaltreetools import BoundedInterval


def _make_test_intervals():

    return [
        BoundedInterval(0, 3,   {'a': 1}),
        BoundedInterval(5, 13,  {'b': 2}),
        BoundedInterval(6, 10,  {'c': 3}),
        BoundedInterval(8, 9,   {'d': 4}),
        BoundedInterval(15, 23, {'e': 5}),
        BoundedInterval(16, 21, {'f': 6}),
        BoundedInterval(17, 19, {'g': 7}),
        BoundedInterval(19, 20, {'h': 8}),
        BoundedInterval(25, 30, {'i': 9}),
        BoundedInterval(26, 29, {'j': 10}),
        BoundedInterval(32, 34, {'k': 11}),
        BoundedInterval(34, 37, {'l': 12}),
    ]
