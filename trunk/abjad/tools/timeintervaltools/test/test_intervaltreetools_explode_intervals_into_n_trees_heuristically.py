from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_01():
    tree = TimeIntervalTree(_make_test_intervals())
    n = 1
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([ \
        TimeInterval(0, 3, {'a': 1}), \
        TimeInterval(5, 13, {'b': 2}), \
        TimeInterval(6, 10, {'c': 3}), \
        TimeInterval(8, 9, {'d': 4}), \
        TimeInterval(15, 23, {'e': 5}), \
        TimeInterval(16, 21, {'f': 6}), \
        TimeInterval(17, 19, {'g': 7}), \
        TimeInterval(19, 20, {'h': 8}), \
        TimeInterval(25, 30, {'i': 9}), \
        TimeInterval(26, 29, {'j': 10}), \
        TimeInterval(32, 34, {'k': 11}), \
        TimeInterval(34, 37, {'l': 12}) \
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])

def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_02():
    tree = TimeIntervalTree(_make_test_intervals())
    n = 2
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([
        TimeInterval(0, 3, {'a': 1}),
        TimeInterval(6, 10, {'c': 3}),
        TimeInterval(8, 9, {'d': 4}),
        TimeInterval(15, 23, {'e': 5}),
        TimeInterval(17, 19, {'g': 7}),
        TimeInterval(19, 20, {'h': 8}),
        TimeInterval(26, 29, {'j': 10})
    ]), TimeIntervalTree([
        TimeInterval(5, 13, {'b': 2}),
        TimeInterval(16, 21, {'f': 6}),
        TimeInterval(25, 30, {'i': 9}),
        TimeInterval(32, 34, {'k': 11}),
        TimeInterval(34, 37, {'l': 12})
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])


def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_03():
    tree = TimeIntervalTree(_make_test_intervals())
    n = 3
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([
        TimeInterval(0, 3, {'a': 1}),
        TimeInterval(8, 9, {'d': 4}),
        TimeInterval(15, 23, {'e': 5}),
        TimeInterval(32, 34, {'k': 11}),
        TimeInterval(34, 37, {'l': 12})
    ]), TimeIntervalTree([
        TimeInterval(5, 13, {'b': 2}),
        TimeInterval(17, 19, {'g': 7}),
        TimeInterval(19, 20, {'h': 8}),
        TimeInterval(26, 29, {'j': 10})
    ]), TimeIntervalTree([
        TimeInterval(6, 10, {'c': 3}),
        TimeInterval(16, 21, {'f': 6}),
        TimeInterval(25, 30, {'i': 9})
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])
