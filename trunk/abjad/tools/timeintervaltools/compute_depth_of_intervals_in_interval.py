from abjad.tools import sequencetools


def compute_depth_of_intervals_in_interval(intervals, bounding_interval):
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
    tree = tree.find_intervals_intersecting_or_tangent_to_interval(
        bounding_interval)
    if not tree:
        return timeintervaltools.TimeIntervalTree([timeintervaltools.TimeInterval(
            bounding_interval.start, bounding_interval.stop, {'depth': 0})])

    all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(
        tree))
    while all_bounds[0] < bounding_interval.start:
        all_bounds.pop(0)
    while bounding_interval.stop < all_bounds[-1]:
        all_bounds.pop()
    if bounding_interval.start < all_bounds[0]:
        all_bounds.insert(0, bounding_interval.start)
    if all_bounds[-1] < bounding_interval.stop:
        all_bounds.append(bounding_interval.stop)

#    if interval.stop <= tree.start or tree.stop <= interval.start:
#        return timeintervaltools.TimeIntervalTree([timeintervaltools.TimeInterval(
#            interval.start, interval.stop, {'depth': 0})])
#    else:
#        all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(tree))
#        if interval.start < tree.start:
#            all_bounds.insert(0, interval.start)
#        elif tree.start < interval.start:
#            all_bounds = [x for x in all_bounds if interval.start <= x]
#            all_bounds.insert(0, interval.start)
#        if tree.stop < interval.stop:
#            all_bounds.append(interval.stop)
#        elif interval.stop < tree.stop:
#            all_bounds = [x for x in all_bounds if x <= interval.stop]
#            all_bounds.append(interval.stop)
#        all_bounds = sorted(list(set(all_bounds)))

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
