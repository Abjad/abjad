from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_intervals_are_nonoverlapping import all_intervals_are_nonoverlapping
from abjad.tools.timeintervaltools.compute_logical_xor_of_intervals import compute_logical_xor_of_intervals
from abjad.tools.timeintervaltools.mask_intervals_with_intervals import mask_intervals_with_intervals
from collections import Iterable


def resolve_overlaps_between_nonoverlapping_trees(trees):
    '''Create a nonoverlapping TimeIntervalTree from `trees`.
    Intervals in higher-indexed trees in `trees` only appear in part or whole where they do not
    overlap intervals from starter-indexed trees ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeIntervalTree(TimeInterval(0, 4, {'a': 1}))
        >>> b = TimeIntervalTree(TimeInterval(1, 5, {'b': 2}))
        >>> c = TimeIntervalTree(TimeInterval(2, 6, {'c': 3}))
        >>> d = TimeIntervalTree(TimeInterval(1, 3, {'d': 4}))
        >>> timeintervaltools.resolve_overlaps_between_nonoverlapping_trees([a, b, c, d])
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(4, 1), {'a': 1}),
            TimeInterval(Offset(4, 1), Offset(5, 1), {'b': 2}),
            TimeInterval(Offset(5, 1), Offset(6, 1), {'c': 3})
        ])

    Return interval tree.
    '''

    assert isinstance(trees, Iterable) and len(trees) \
        and all([isinstance(x, TimeIntervalTree) for x in trees]) \
        and all([all_intervals_are_nonoverlapping(x) for x in trees])

    rtree = trees[0]
    for tree in trees[1:]:
        xor = compute_logical_xor_of_intervals([tree, rtree])
        masked = mask_intervals_with_intervals(tree, xor)
        rtree._insert(masked)

    assert all_intervals_are_nonoverlapping(rtree)

    return rtree
