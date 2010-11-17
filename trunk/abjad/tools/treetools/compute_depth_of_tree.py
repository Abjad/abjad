from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.get_all_unique_bounds_in_tree \
    import get_all_unique_bounds_in_tree


def compute_depth_of_tree(tree):
    assert isinstance(tree, IntervalTree)
    values = get_all_unique_bounds_in_tree(tree)
    intervals = [ ]
    for i in range(len(values[1:])):
        found_a = set(tree.find_intervals_intersecting_or_tangent_to_interval(values[i], values[i + 1]))
        found_b = set(tree.find_intervals_starting_at_offset(values[i + 1]))
        found_c = set(tree.find_intervals_stopping_at_offset(values[i]))
        found = found_a.difference(found_b)
        found = tuple(found.difference(found_c))
        zeros = filter(lambda x: x.low == x.high, found_c)
        if zeros:
            intervals.append(BoundedInterval(values[i], values[i], {'depth': len(found) + len(zeros)}))
        intervals.append(BoundedInterval(values[i], values[i + 1], {'depth': len(found)}))
    return IntervalTree(intervals)
