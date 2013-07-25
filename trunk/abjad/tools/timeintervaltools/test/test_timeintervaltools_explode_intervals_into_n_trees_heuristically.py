from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_explode_intervals_into_n_trees_heuristically_01():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    n = 1
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([
        TimeInterval(0, 3,   {'name': 'a'}),
        TimeInterval(5, 13,  {'name': 'b'}),
        TimeInterval(6, 10,  {'name': 'c'}),
        TimeInterval(8, 9,   {'name': 'd'}),
        TimeInterval(15, 23, {'name': 'e'}),
        TimeInterval(16, 21, {'name': 'f'}),
        TimeInterval(17, 19, {'name': 'g'}),
        TimeInterval(19, 20, {'name': 'h'}),
        TimeInterval(25, 30, {'name': 'i'}),
        TimeInterval(26, 29, {'name': 'j'}),
        TimeInterval(32, 34, {'name': 'k'}),
        TimeInterval(34, 37, {'name': 'l'})
    ])]
    if n == tree.calculate_minimum_mean_and_maximum_depths()[2]:
        assert all(x.intervals_are_nonoverlapping for x in result)

def test_timeintervaltools_explode_intervals_into_n_trees_heuristically_02():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    n = 2
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([
        TimeInterval(0, 3,   {'name': 'a'}),
        TimeInterval(6, 10,  {'name': 'c'}),
        TimeInterval(8, 9,   {'name': 'd'}),
        TimeInterval(15, 23, {'name': 'e'}),
        TimeInterval(17, 19, {'name': 'g'}),
        TimeInterval(19, 20, {'name': 'h'}),
        TimeInterval(26, 29, {'name': 'j'})
    ]), TimeIntervalTree([
        TimeInterval(5, 13,  {'name': 'b'}),
        TimeInterval(16, 21, {'name': 'f'}),
        TimeInterval(25, 30, {'name': 'i'}),
        TimeInterval(32, 34, {'name': 'k'}),
        TimeInterval(34, 37, {'name': 'l'})
    ])]
    if n == tree.calculate_minimum_mean_and_maximum_depths()[2]:
        assert all(x.intervals_are_nonoverlapping for x in result)


def test_timeintervaltools_explode_intervals_into_n_trees_heuristically_03():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    n = 3
    result = explode_intervals_into_n_trees_heuristically(tree, n)
    assert result == \
    [TimeIntervalTree([
        TimeInterval(0, 3,   {'name': 'a'}),
        TimeInterval(8, 9,   {'name': 'd'}),
        TimeInterval(15, 23, {'name': 'e'}),
        TimeInterval(32, 34, {'name': 'k'}),
        TimeInterval(34, 37, {'name': 'l'})
    ]), TimeIntervalTree([
        TimeInterval(5, 13,  {'name': 'b'}),
        TimeInterval(17, 19, {'name': 'g'}),
        TimeInterval(19, 20, {'name': 'h'}),
        TimeInterval(26, 29, {'name': 'j'})
    ]), TimeIntervalTree([
        TimeInterval(6, 10,  {'name': 'c'}),
        TimeInterval(16, 21, {'name': 'f'}),
        TimeInterval(25, 30, {'name': 'i'})
    ])]
    if n == tree.calculate_minimum_mean_and_maximum_depths()[2]:
        assert all(x.intervals_are_nonoverlapping for x in result)
