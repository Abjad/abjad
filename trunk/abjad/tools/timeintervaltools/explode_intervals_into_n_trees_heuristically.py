from abjad.tools import durationtools


def explode_intervals_into_n_trees_heuristically(intervals, n):
    '''Explode `intervals` into `n` trees, avoiding overlap when possible,
    and distributing intervals so as to equalize density across the trees.

    Return list of TimeIntervalTree instances.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return [timeintervaltools.TimeIntervalTree([])] * n
    elif n == 1:
        return [tree]

    # cache
    treebounds = timeintervaltools.TimeInterval(tree.start, tree.stop)
    xtrees = [timeintervaltools.TimeIntervalTree(tree[0])]
    densities = [timeintervaltools.calculate_depth_density_of_intervals_in_interval(
        xtrees[0], treebounds)]
    logical_ors = [timeintervaltools.compute_logical_or_of_intervals(xtrees[0])]
    for i in range(1, n):
        xtrees.append(timeintervaltools.TimeIntervalTree([]))
        densities.append(0)
        logical_ors.append(timeintervaltools.TimeIntervalTree([]))

    # loop through intervals
    for interval in tree[1:]:

        empty_trees = []
        nonoverlapping_trees = []
        overlapping_trees = []

        for i, zipped in enumerate(zip(xtrees, densities, logical_ors)):
            xtree = zipped[0]
            density = zipped[1]
            logical_or = zipped[2]
            if not len(xtree):
                empty_trees.append((i, xtree, density, logical_or))
                break
            elif not logical_or[-1].is_overlapped_by_interval(interval):
                nonoverlapping_trees.append((i, xtree, density, logical_or))
            else:
                overlapping_trees.append((i, xtree, density, logical_or))

        if len(empty_trees):
            i = empty_trees[0][0]
        elif len(nonoverlapping_trees):
            nonoverlapping_trees = sorted(nonoverlapping_trees, key=lambda x: x[2])
            i = nonoverlapping_trees[0][0]
        else:
            overlapping_trees = sorted(overlapping_trees, \
                key = lambda x: x[3][-1].get_overlap_with_interval(interval))
            overlapping_trees = [x for x in overlapping_trees \
                if x[3][-1].duration == overlapping_trees[0][3][-1].duration]
            i = overlapping_trees[0][0]

        xtrees[i]._insert(interval)
        densities[i] = timeintervaltools.calculate_depth_density_of_intervals_in_interval(xtrees[i], treebounds)
        logical_ors[i] = timeintervaltools.compute_logical_or_of_intervals(xtrees[i])

    return xtrees
