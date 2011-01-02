from abjad import *
from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.compute_depth_of_tree import compute_depth_of_tree
from abjad.tools.treetools.explode_overlapping_tree_into_nonoverlapping_trees_uncompactly \
    import explode_overlapping_tree_into_nonoverlapping_trees_uncompactly
from abjad.tools.treetools.shift_tree_to_value import shift_tree_to_value


def make_percussion_score_of_tree(tree):

    assert isinstance(tree, IntervalTree)

    filtered_tree = IntervalTree([interval for interval in tree if 0 < interval.magnitude])
    shifted_tree = shift_tree_to_value(filtered_tree, 0)
    xtrees = explode_overlapping_tree_into_nonoverlapping_trees_uncompactly(shifted_tree)
    dtrees = [compute_depth_of_tree(xtree) for xtree in xtrees]
    for dtree in dtrees:
        if 0 < dtree.low_min:
            dtree.insert(BoundedInterval(0, dtree.low_min, {'depth': 0}))

    staves = stafftools.RhythmicStaff([ ]) * len(dtrees)

    for pair in zip(staves, dtrees):
        for interval in pair[1]:
            con = Container([ ])
            if interval.data['depth']:
                con.extend(leaftools.make_leaves([0], [interval.magnitude]))
            else:
                con.extend(resttools.make_rests([interval.magnitude]))
            pair[0].append(con)

    return Score(staves)
