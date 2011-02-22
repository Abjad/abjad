from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree


def split_intervals_at_offsets(tree, values):
    '''Return a new `IntervalTree` where all intervals in `tree` have
    been split at each value in `values` ::

        abjad> tree = IntervalTree([ ])
        abjad> tree.insert(BoundedInterval(0, 10, 'a'))
        abjad> tree.insert(BoundedInterval(5, 15, 'b'))
        abjad> split_intervals_at_offsets(tree, [-1, 3, 7, 16])
        IntervalTree([
            BoundedInterval(0, 3, data = 'a'),
            BoundedInterval(3, 7, data = 'a'),
            BoundedInterval(5, 7, data = 'b'),
            BoundedInterval(7, 10, data = 'a'),
            BoundedInterval(7, 15, data = 'b')
        ])
    '''

    assert isinstance(tree, IntervalTree)
    assert len(values)
    assert all([isinstance(x, (int, Fraction)) for x in values])

    if all([value <= tree.low_min or tree.high_max <= value \
            for value in values]):
        return tree

    output_tree = IntervalTree(tree)

    for value in values:
        intervals_to_remove = [ ]
        intervals_to_insert = [ ]
        intervals = output_tree.find_intervals_intersecting_or_tangent_to_offset(value)
        for interval in intervals:
            splits = interval.split_at_value(value)
            if len(splits) == 2:
                intervals_to_remove.append(interval)
                intervals_to_insert.extend(splits)
        output_intervals = set(output_tree).union(set(intervals_to_insert))
        output_intervals = set(output_intervals).difference(set(intervals_to_remove))
        output_tree = IntervalTree(output_intervals)

    return output_tree
