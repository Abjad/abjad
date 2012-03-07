from abjad.tools.intervaltreetools import TimeInterval
from abjad.tools.intervaltreetools import IntervalTree
from abjad.tools.intervaltreetools import resolve_overlaps_between_nonoverlapping_trees


def test_intervaltreetools_resolve_overlaps_between_nonoverlapping_trees_01():
    a = IntervalTree(TimeInterval(0, 4, {'a': 1}))
    b = IntervalTree(TimeInterval(1, 5, {'b': 2}))
    c = IntervalTree(TimeInterval(2, 6, {'c': 3}))
    d = IntervalTree(TimeInterval(1, 3, {'d': 4}))
    result = resolve_overlaps_between_nonoverlapping_trees([a, b, c, d])
    assert result == \
    IntervalTree([
        TimeInterval(0, 4, {'a': 1}),
        TimeInterval(4, 5, {'b': 2}),
        TimeInterval(5, 6, {'c': 3})
    ])
