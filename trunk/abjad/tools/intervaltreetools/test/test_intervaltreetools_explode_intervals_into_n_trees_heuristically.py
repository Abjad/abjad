from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_01():
    tree = IntervalTree(_make_test_intervals())
    n = 1
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [IntervalTree([ \
        BoundedInterval(0, 3, {'a': 1}), \
        BoundedInterval(5, 13, {'b': 2}), \
        BoundedInterval(6, 10, {'c': 3}), \
        BoundedInterval(8, 9, {'d': 4}), \
        BoundedInterval(15, 23, {'e': 5}), \
        BoundedInterval(16, 21, {'f': 6}), \
        BoundedInterval(17, 19, {'g': 7}), \
        BoundedInterval(19, 20, {'h': 8}), \
        BoundedInterval(25, 30, {'i': 9}), \
        BoundedInterval(26, 29, {'j': 10}), \
        BoundedInterval(32, 34, {'k': 11}), \
        BoundedInterval(34, 37, {'l': 12}) \
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])

def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_02():
    tree = IntervalTree(_make_test_intervals())
    n = 2
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [IntervalTree([
        BoundedInterval(0, 3, {'a': 1}),
        BoundedInterval(6, 10, {'c': 3}),
        BoundedInterval(8, 9, {'d': 4}),
        BoundedInterval(15, 23, {'e': 5}),
        BoundedInterval(17, 19, {'g': 7}),
        BoundedInterval(19, 20, {'h': 8}),
        BoundedInterval(26, 29, {'j': 10})
    ]), IntervalTree([
        BoundedInterval(5, 13, {'b': 2}),
        BoundedInterval(16, 21, {'f': 6}),
        BoundedInterval(25, 30, {'i': 9}),
        BoundedInterval(32, 34, {'k': 11}),
        BoundedInterval(34, 37, {'l': 12})
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])


def test_intervaltreetools_explode_intervals_into_n_trees_heuristically_03():
    tree = IntervalTree(_make_test_intervals())
    n = 3
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [IntervalTree([
        BoundedInterval(0, 3, {'a': 1}),
        BoundedInterval(8, 9, {'d': 4}),
        BoundedInterval(15, 23, {'e': 5}),
        BoundedInterval(32, 34, {'k': 11}),
        BoundedInterval(34, 37, {'l': 12})
    ]), IntervalTree([
        BoundedInterval(5, 13, {'b': 2}),
        BoundedInterval(17, 19, {'g': 7}),
        BoundedInterval(19, 20, {'h': 8}),
        BoundedInterval(26, 29, {'j': 10})
    ]), IntervalTree([
        BoundedInterval(6, 10, {'c': 3}),
        BoundedInterval(16, 21, {'f': 6}),
        BoundedInterval(25, 30, {'i': 9})
    ])]
    if n == calculate_min_mean_and_max_depth_of_intervals(tree)[2]:
        assert all([all_intervals_are_nonoverlapping(x) for x in result])
