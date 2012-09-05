def calculate_min_mean_and_max_depth_of_intervals(intervals):
    '''Return a 3-tuple of the minimum, mean and maximum depth of `intervals`.
    If `intervals` is empty, return None.  "Mean" in this case is a weighted mean,
    where the durations of the intervals in depth tree of `intervals` are the weights
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    depth_tree = timeintervaltools.compute_depth_of_intervals(tree)
    depths = [x['depth'] for x in depth_tree]
    mean = timeintervaltools.calculate_depth_density_of_intervals(tree)
    return min(depths), mean, max(depths)
