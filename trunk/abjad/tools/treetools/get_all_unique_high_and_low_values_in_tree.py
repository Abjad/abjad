from abjad.tools.treetools import IntervalTree


def get_all_unique_high_and_low_values_in_tree(tree):
    assert isinstance(tree, IntervalTree)
    values = [ ]
    for interval in tree.intervals:
        if interval.low not in values:
            values.append(interval.low)
        if interval.high not in values:
            values.append(interval.high)
    return tuple(sorted(values))
