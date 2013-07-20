from abjad.tools import sequencetools


def compute_depth_of_intervals(intervals):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`::

        >>> from abjad.tools.timeintervaltools import *
        >>> a = TimeInterval(0, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 15)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> compute_depth_of_intervals(tree)
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1})
        ])

    Return interval tree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(tree))
    depth_intervals = []
    for start, stop in sequencetools.iterate_sequence_pairwise_strict(
        all_bounds):
        current_interval = timeintervaltools.TimeInterval(start, stop, {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(
            current_interval)
        depth = 0
        if found:
            depth = len([x for x in found 
                if (not x.start == current_interval.stop 
                and not x.stop == current_interval.start)])
        current_interval['depth'] = depth
        depth_intervals.append(current_interval)

    return timeintervaltools.TimeIntervalTree(depth_intervals)
