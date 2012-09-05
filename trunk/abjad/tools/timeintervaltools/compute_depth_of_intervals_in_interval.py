from abjad.tools import sequencetools


def compute_depth_of_intervals_in_interval(intervals, interval):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`, cropped within `interval`::

        >>> from abjad.tools.timeintervaltools import *
        >>> a = TimeInterval(0, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 15)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> d = TimeInterval(-1, 16)
        >>> compute_depth_of_intervals_in_interval(tree, d)
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(0, 1), {'depth': 0}),
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1}),
            TimeInterval(Offset(15, 1), Offset(16, 1), {'depth': 0})
        ])

    Return interval tree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if interval.stop <= tree.start or tree.stop <= interval.start:
        return timeintervaltools.TimeIntervalTree([timeintervaltools.TimeInterval(
            interval.start, interval.stop, {'depth': 0})])
    else:
        bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(tree))
        if interval.start < tree.start:
            bounds.insert(0, interval.start)
        elif tree.start < interval.start:
            bounds = [x for x in bounds if interval.start <= x]
            bounds.insert(0, interval.start)
        if tree.stop < interval.stop:
            bounds.append(interval.stop)
        elif interval.stop < tree.stop:
            bounds = [x for x in bounds if x <= interval.stop]
            bounds.append(interval.stop)
        bounds = sorted(list(set(bounds)))

    intervals = []
    for pair in sequencetools.iterate_sequence_pairwise_strict(bounds):
        target = timeintervaltools.TimeInterval(pair[0], pair[1], {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
        if found:
            target['depth'] = len([x for x in found
                if (not x.start == target.stop and not x.stop == target.start)])
        else:
            target['depth'] = 0
        intervals.append(target)

    return timeintervaltools.TimeIntervalTree(intervals)
