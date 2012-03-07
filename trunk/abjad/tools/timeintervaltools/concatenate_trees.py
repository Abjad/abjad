from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.shift_aggregate_offset_to_rational import shift_aggregate_offset_to_rational
from abjad import Fraction


def concatenate_trees(trees, padding = 0):
    '''Merge all trees in `trees`, offsetting each subsequent tree
    to start after the previous.'''

    assert all([isinstance(tree, TimeIntervalTree) for tree in trees])
    assert isinstance(padding, (int, Fraction))
    assert 0 <= padding

    output_tree = TimeIntervalTree(shift_aggregate_offset_to_rational(trees[0], 0))
    for tree in trees[1:]:
        output_tree = TimeIntervalTree([
            output_tree,
            shift_aggregate_offset_to_rational(tree, output_tree.latest_stop + padding)
        ])

    return output_tree
