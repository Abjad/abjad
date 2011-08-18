from abjad.tools.intervaltreetools import BoundedInterval
from abjad.tools.intervaltreetools import IntervalTree
from abjad.tools.intervaltreetools import resolve_overlaps_between_nonoverlapping_trees


def test_intervaltreetools_resolve_overlaps_between_nonoverlapping_trees_01():
    a = IntervalTree(BoundedInterval(0, 4, {'a': 1}))
    b = IntervalTree(BoundedInterval(1, 5, {'b': 2}))
    c = IntervalTree(BoundedInterval(2, 6, {'c': 3}))
    d = IntervalTree(BoundedInterval(1, 3, {'d': 4}))
    result = resolve_overlaps_between_nonoverlapping_trees([a, b, c, d])
    assert result == \
    IntervalTree([
        BoundedInterval(0, 4, {'a': 1}),
        BoundedInterval(4, 5, {'b': 2}),
        BoundedInterval(5, 6, {'c': 3})
    ])
