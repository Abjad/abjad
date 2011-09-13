from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.leaftools.set_preprolated_leaf_duration import set_preprolated_leaf_duration
from abjad.tools import durationtools


def _split_leaf_at_duration(leaf, split_dur, spanners = 'unfractured', tie_after = False):
    '''Split leaf into left and right lists.
    Left list may be list of one note, many tied notes, or tuplet.
    Right list may be list of one note, many tied notes, or tuplet.
    Interpret boolean tie_after keyword as 'add tie after split'.
    Return value is always uniformly a pair of lists.
    '''
    from abjad.tools import contexttools
    from abjad.tools import componenttools
    from abjad.tools import spannertools
    from abjad.tools import tietools

    assert isinstance(leaf, _Leaf)
    split_dur = durationtools.Duration(split_dur)

    leaf_multiplied_duration = leaf.multiplied_duration
    unprolated_split_dur = split_dur / leaf.prolation

    # handle split duration boundary cases
    if unprolated_split_dur <= 0:
        return ([], [leaf])
    if leaf_multiplied_duration <= unprolated_split_dur:
        return ([leaf], [])

    new_leaf = componenttools.copy_components_and_remove_all_spanners([leaf])[0]
    componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, [new_leaf])
    #new_leaf.grace[:] = []
    if hasattr(new_leaf, 'grace'):
        delattr(new_leaf, '_grace')
        delattr(new_leaf, 'grace')
    # TODO: maybe replace with logic to move marktools.Articulation #
    #new_leaf.articulations[:] = []
    contexttools.detach_context_marks_attached_to_component(new_leaf,
        klasses = (contexttools.DynamicMark, ))
    #leaf.after_grace[:] = []
    if hasattr(leaf, 'after_grace'):
        delattr(leaf, '_after_grace')
        delattr(leaf, 'after_grace')

    left_leaf_list = set_preprolated_leaf_duration(leaf, unprolated_split_dur)
    right_leaf_list = set_preprolated_leaf_duration(
        new_leaf, leaf_multiplied_duration - unprolated_split_dur)

    leaf_left_of_split = left_leaf_list[-1]
    leaf_right_of_split = right_leaf_list[0]

    if spanners == 'fractured':
        #leaf_left_of_split.spanners.fracture(direction = 'right')
        spannertools.fracture_all_spanners_attached_to_component(
            leaf_left_of_split, direction = 'right')
    elif spanners == 'unfractured':
        pass
    else:
        raise ValueError("keyword must be 'fractured' or 'unfractured'.")

    if tie_after:
        tietools.apply_tie_spanner_to_leaf_pair(leaf_left_of_split, leaf_right_of_split)

    return left_leaf_list, right_leaf_list
