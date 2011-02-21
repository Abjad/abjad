from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.shift_tree_to_value import shift_tree_to_value


def concatenate_trees(trees, padding = 0):
    '''Merge all trees in `trees`, offsetting each subsequent tree
    to start after the previous.'''

    pass

    assert all([isinstance(tree, IntervalTree) for tree in trees])
    assert isinstance(padding, (int, Fraction))
    assert 0 <= padding

    output_tree = IntervalTree(shift_tree_to_value(trees[0], 0))
    for tree in trees[1:]:
#        output_tree.insert(shift_tree_to_value(tree, output_tree.high_max + padding))
        output_tree = IntervalTree([
            output_tree,
            shift_tree_to_value(tree, output_tree.high_max + padding)
        ])    

    return output_tree
