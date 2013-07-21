from abjad.tools import sequencetools


def compute_depth_of_intervals(intervals, bounding_interval=None):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`::

        >>> a = timeintervaltools.TimeInterval(0, 3)
        >>> b = timeintervaltools.TimeInterval(6, 12)
        >>> c = timeintervaltools.TimeInterval(9, 15)
        >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
        >>> timeintervaltools.compute_depth_of_intervals(tree)
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1})
        ])

    If `bounding_interval` is not none, only consider that time interval:

        >>> a = timeintervaltools.TimeInterval(0, 3)
        >>> b = timeintervaltools.TimeInterval(6, 12)
        >>> c = timeintervaltools.TimeInterval(9, 15)
        >>> tree = timeintervaltools.TimeIntervalTree([a, b, c])
        >>> d = timeintervaltools.TimeInterval(-1, 16)
        >>> timeintervaltools.compute_depth_of_intervals(tree, bounding_interval=d)
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

    if bounding_interval is not None:
        tree = tree.find_intervals_intersecting_or_tangent_to_interval(
            bounding_interval)
        if not tree:
            return timeintervaltools.TimeIntervalTree([
                timeintervaltools.TimeInterval(
                    bounding_interval.start_offset, 
                    bounding_interval.stop_offset, 
                    {'depth': 0},
                    )
                ])
        all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(
            tree))
        while all_bounds[0] < bounding_interval.start_offset:
            all_bounds.pop(0)
        while bounding_interval.stop_offset < all_bounds[-1]:
            all_bounds.pop()
        if bounding_interval.start_offset < all_bounds[0]:
            all_bounds.insert(0, bounding_interval.start_offset)
        if all_bounds[-1] < bounding_interval.stop_offset:
            all_bounds.append(bounding_interval.stop_offset)
    else:
        all_bounds = list(timeintervaltools.get_all_unique_bounds_in_intervals(
            tree))
    
    depth_intervals = []
    for start_offset, stop_offset in sequencetools.iterate_sequence_pairwise_strict(
        all_bounds):
        current_interval = timeintervaltools.TimeInterval(start_offset, stop_offset, {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(
            current_interval)
        depth = 0
        if found:
            depth = len([x for x in found 
                if (not x.start_offset == current_interval.stop_offset 
                and not x.stop_offset == current_interval.start_offset)])
        current_interval['depth'] = depth
        depth_intervals.append(current_interval)

    return timeintervaltools.TimeIntervalTree(depth_intervals)
