def explode_intervals_uncompactly(intervals):
    '''Explode the intervals in `intervals` into n non-overlapping trees,
    where n is the maximum depth of `intervals`.

    The algorithm will attempt to insert the exploded intervals
    cyclically, making its insertion attempt at the next resultant tree
    in the array, rather than always beginning its search from index 0.

    Return list of `TimeIntervalTree` instances.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    depth_tree = timeintervaltools.compute_depth_of_intervals(tree)
    max_depth = max([x['depth'] for x in depth_tree])
    layers = [[] for i in range(max_depth)]

    offset = 0
    for interval in tree:
        for i in range(max_depth):
            layer = layers[(i + offset) % max_depth]
            if not len(layer):
                layer.append(interval)
                offset = i + 1
                break
            elif not layer[-1].is_overlapped_by_interval(interval):
                layer.append(interval)
                offset = i + 1
                break

    return [timeintervaltools.TimeIntervalTree(layer) for layer in layers]
