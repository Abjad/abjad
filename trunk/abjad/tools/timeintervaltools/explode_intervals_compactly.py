def explode_intervals_compactly(intervals):
    '''Explode the intervals in `intervals` into n non-overlapping trees,
    where n is the maximum depth of `intervals`.

    The algorithm will attempt to insert the exploded intervals
    into the lowest-indexed resultant tree with free space.

    Return an array of `TimeIntervalTree` instances.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    depth_tree = timeintervaltools.compute_depth_of_intervals(tree)
    max_depth = max([x['depth'] for x in depth_tree])

    layers = [[] for _ in range(max_depth)]
    
    for interval in tree:
        for layer in layers:
            if not len(layer):
                layer.append(interval)
                break
            elif not layer[-1].is_overlapped_by_interval(interval):
                layer.append(interval)
                break

    return [timeintervaltools.TimeIntervalTree(layer) for layer in layers]
