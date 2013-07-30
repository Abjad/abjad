from abjad.tools import durationtools


def explode_intervals(tree, aggregate_count=None):
    '''Explode intervals into trees, avoiding overlap and distributing
    density.

    Example 1. Explode intervals into optimal number of non-overlapping trees:

    ::

        >>> tree = timeintervaltools.TimeIntervalTree(
        ...     timeintervaltools.make_test_intervals())
        >>> tree
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
            TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
            TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
            TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
            TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
            TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
            TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
            TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
            TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
            TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
            TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'}),
            TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
        ])

    ::

        >>> exploded_trees = timeintervaltools.explode_intervals(tree)
        >>> for exploded_tree in exploded_trees:
        ...     exploded_tree
        ...
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
            TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
            TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
            TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
            TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
            TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
            TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
            TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
            TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
            TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
        ])

    Example 2. Explode intervals into less-than-optimal number of overlapping
    trees:

    ::

        >>> exploded_trees = timeintervaltools.explode_intervals(tree,
        ...     aggregate_count=2)
        >>> for exploded_tree in exploded_trees:
        ...     exploded_tree
        ...
        TimeIntervalTree([
            TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'}),
            TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'}),
            TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
            TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
            TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
            TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'}),
            TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
            TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'}),
            TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
            TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
            TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
        ])

    Example 3. Explode intervals into greater-than-optimal number of 
    non-overlapping trees:

    ::

        >>> exploded_trees = timeintervaltools.explode_intervals(tree,
        ...     aggregate_count=6)
        >>> for exploded_tree in exploded_trees:
        ...     exploded_tree
        ...
        TimeIntervalTree([
            TimeInterval(Offset(16, 1), Offset(21, 1), {'name': 'f'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(15, 1), Offset(23, 1), {'name': 'e'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(8, 1), Offset(9, 1), {'name': 'd'}),
            TimeInterval(Offset(17, 1), Offset(19, 1), {'name': 'g'}),
            TimeInterval(Offset(19, 1), Offset(20, 1), {'name': 'h'}),
            TimeInterval(Offset(25, 1), Offset(30, 1), {'name': 'i'}),
            TimeInterval(Offset(34, 1), Offset(37, 1), {'name': 'l'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(6, 1), Offset(10, 1), {'name': 'c'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(5, 1), Offset(13, 1), {'name': 'b'})
        ])
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'a'}),
            TimeInterval(Offset(26, 1), Offset(29, 1), {'name': 'j'}),
            TimeInterval(Offset(32, 1), Offset(34, 1), {'name': 'k'})
        ])

    Return 0 or more trees.
    '''
    from abjad.tools import timeintervaltools

    assert isinstance(aggregate_count, (type(None), int))
    if isinstance(aggregate_count, int):
        assert 0 < aggregate_count

    if not len(tree):
        return []

    bounding_interval = timeintervaltools.TimeInterval(
        tree.start_offset, tree.stop_offset)
    global_densities = []
    empty_tree_pairs = []
    exploded_trees = []
    if aggregate_count is not None:
        for i in xrange(aggregate_count):
            global_densities.append(0)
            exploded_tree = timeintervaltools.TimeIntervalTree()
            empty_tree_pairs.append((i, exploded_tree))
            exploded_trees.append(exploded_tree)

    for current_interval in tree:

        if empty_tree_pairs:
            i, empty_tree = empty_tree_pairs.pop()
            empty_tree._insert(current_interval)
            global_densities[i] = empty_tree.calculate_depth_density(
                bounding_interval=bounding_interval)
            continue
            
        nonoverlapping_trees = []
        overlapping_trees = []
        for i, exploded_tree in enumerate(exploded_trees):
            local_density = exploded_tree.calculate_depth_density(
                bounding_interval=current_interval)
            global_density = global_densities[i]
            if not local_density:
                nonoverlapping_trees.append((i, global_density)) 
            else:
                overlapping_trees.append((i, local_density, global_density))
        nonoverlapping_trees.sort(key=lambda x: x[1])
        overlapping_trees.sort(key=lambda x: (x[1], x[2]))

        if not nonoverlapping_trees and aggregate_count is None:
            exploded_tree = timeintervaltools.TimeIntervalTree(
                [current_interval])
            global_densities.append(exploded_tree.calculate_depth_density(
                bounding_interval=bounding_interval))
            exploded_trees.append(exploded_tree)
            continue

        if nonoverlapping_trees:
            i = nonoverlapping_trees[0][0]
        else:
            i = overlapping_trees[0][0]
        exploded_tree = exploded_trees[i]
        global_densities[i] = exploded_tree.calculate_depth_density(
            bounding_interval=bounding_interval)
        exploded_tree._insert(current_interval)

    return tuple(exploded_trees)
