from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.build_tree_of_depth_of_tree \
    import build_tree_of_depth_of_tree


def build_tree_of_empty_intervals_in_tree(tree):
    assert isinstance(tree, IntervalTree)
    depths = build_tree_of_depth_of_tree(tree)
    empties = IntervalTree(filter(lambda x: not x.data['depth'], depths))
    return empties
