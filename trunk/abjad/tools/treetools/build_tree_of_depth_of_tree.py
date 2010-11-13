from abjad.tools.treetools import *
from abjad.tools.treetools._Interval import _Interval
from abjad.tools.treetools.get_all_unique_high_and_low_values_in_tree \
    import get_all_unique_high_and_low_values_in_tree


def build_tree_of_depth_of_tree(tree):
    assert isinstance(tree, IntervalTree)
    values = get_all_unique_high_and_low_values_in_tree(tree)
    intervals = [ ]
    for i in range(len(values[1:])):
        found_a = set(tree.find_intervals_intersecting_or_tangent_to_interval(values[i], values[i + 1]))
        found_b = set(tree.find_intervals_starting_at_offset(values[i + 1]))
        found_c = set(tree.find_intervals_stopping_at_offset(values[i]))
        found = found_a.difference(found_b)
        found = tuple(found.difference(found_c))
        zeros = filter(lambda x: x.low == x.high, found_c)
        if zeros:
            intervals.append(_Interval(values[i], values[i], {'depth': len(found) + len(zeros)}))
        intervals.append(_Interval(values[i], values[i + 1], {'depth': len(found)}))
    return IntervalTree(intervals)
