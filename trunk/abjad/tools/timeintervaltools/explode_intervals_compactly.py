from abjad.tools.timeintervaltools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def explode_intervals_compactly(intervals):
    '''Explode the intervals in `intervals` into n non-overlapping trees,
    where n is the maximum depth of `intervals`.

    Returns an array of `TimeIntervalTree` instances.

    The algorithm will attempt to insert the exploded intervals
    into the lowest-indexed resultant tree with free space.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    depth_tree = compute_depth_of_intervals(tree)
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

    return [TimeIntervalTree(layer) for layer in layers]
