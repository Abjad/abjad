from abjad.tools.intervaltreetools import TimeInterval


def _make_test_intervals():

    return [
        TimeInterval(0, 3,   {'a': 1}),
        TimeInterval(5, 13,  {'b': 2}),
        TimeInterval(6, 10,  {'c': 3}),
        TimeInterval(8, 9,   {'d': 4}),
        TimeInterval(15, 23, {'e': 5}),
        TimeInterval(16, 21, {'f': 6}),
        TimeInterval(17, 19, {'g': 7}),
        TimeInterval(19, 20, {'h': 8}),
        TimeInterval(25, 30, {'i': 9}),
        TimeInterval(26, 29, {'j': 10}),
        TimeInterval(32, 34, {'k': 11}),
        TimeInterval(34, 37, {'l': 12}),
    ]
