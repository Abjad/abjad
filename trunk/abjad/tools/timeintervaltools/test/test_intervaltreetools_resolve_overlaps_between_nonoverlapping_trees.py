from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree
from abjad.tools.timeintervaltools import resolve_overlaps_between_nonoverlapping_trees


def test_timeintervaltools_resolve_overlaps_between_nonoverlapping_trees_01():
    a = TimeIntervalTree(TimeInterval(0, 4, {'a': 1}))
    b = TimeIntervalTree(TimeInterval(1, 5, {'b': 2}))
    c = TimeIntervalTree(TimeInterval(2, 6, {'c': 3}))
    d = TimeIntervalTree(TimeInterval(1, 3, {'d': 4}))
    result = resolve_overlaps_between_nonoverlapping_trees([a, b, c, d])
    assert result == \
    TimeIntervalTree([
        TimeInterval(0, 4, {'a': 1}),
        TimeInterval(4, 5, {'b': 2}),
        TimeInterval(5, 6, {'c': 3})
    ])
