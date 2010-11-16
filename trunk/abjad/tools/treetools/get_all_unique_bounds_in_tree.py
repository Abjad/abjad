from abjad.tools.treetools.IntervalTree import IntervalTree


def get_all_unique_bounds_in_tree(tree):
    assert isinstance(tree, IntervalTree)
    values = [ ]
    for interval in tree.intervals:
        if interval.low not in values:
            values.append(interval.low)
        if interval.high not in values:
            values.append(interval.high)
    return tuple(sorted(values))
