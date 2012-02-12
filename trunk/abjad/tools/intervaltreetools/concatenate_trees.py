from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.shift_aggregate_offset_to_rational import shift_aggregate_offset_to_rational
from abjad import Fraction


def concatenate_trees(trees, padding = 0):
    '''Merge all trees in `trees`, offsetting each subsequent tree
    to start after the previous.'''

    assert all([isinstance(tree, IntervalTree) for tree in trees])
    assert isinstance(padding, (int, Fraction))
    assert 0 <= padding

    output_tree = IntervalTree(shift_aggregate_offset_to_rational(trees[0], 0))
    for tree in trees[1:]:
        output_tree = IntervalTree([
            output_tree,
            shift_aggregate_offset_to_rational(tree, output_tree.latest_stop + padding)
        ])

    return output_tree
