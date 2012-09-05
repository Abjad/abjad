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

    bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(tree))
    intervals = []
    for i in range(len(bounds) - 1):
        target = timeintervaltools.TimeInterval(bounds[i], bounds[i+1], {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
        if found:
            depth = len([x for x in found \
                if (not x.start == target.stop and not x.stop == target.start)])
        else:
            depth = 0
        target['depth'] = depth
        intervals.append(target)

    return timeintervaltools.TimeIntervalTree(intervals)
