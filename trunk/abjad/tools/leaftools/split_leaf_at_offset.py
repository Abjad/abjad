from abjad.tools import durationtools


def split_leaf_at_offset(leaf, offset, fracture_spanners=False, tie_after=False):
    r'''Split `leaf` at `offset`.

    .. note:: Replace `tie_after` with `tie_split_notes=True` and `tie_split_rests=False`.

    Example 1. Split note at assignable offset. Two notes result. Do not tie notes::

        >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
        >>> beamtools.apply_beam_spanners_to_measures_in_expr(staff)
        [BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|)]
        >>> contexttools.DynamicMark('f')(staff.leaves[0])
        DynamicMark('f')(c'8)
        >>> marktools.Articulation('accent')(staff.leaves[0])
        Articulation('accent')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 -\accent \f [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> leaftools.split_leaf_at_offset(staff.leaves[0], (1, 32))
        ([Note("c'32")], [Note("c'16.")])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'32 -\accent \f [ (
                c'16.
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    Return pair.
    '''
    from abjad.tools import contexttools
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    from abjad.tools import marktools
    from abjad.tools import spannertools
    from abjad.tools import tietools

    assert isinstance(leaf, leaftools.Leaf)
    offset = durationtools.Duration(offset)

    leaf_multiplied_duration = leaf.multiplied_duration
    unprolated_offset = offset / leaf.prolation

    # handle split duration boundary cases
    if unprolated_offset <= 0:
        return ([], [leaf])
    if leaf_multiplied_duration <= unprolated_offset:
        return ([leaf], [])

    new_leaf = componenttools.copy_components_and_remove_spanners([leaf])[0]
    componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, [new_leaf])
    #new_leaf.grace[:] = []
    if hasattr(new_leaf, 'grace'):
        delattr(new_leaf, '_grace')
        delattr(new_leaf, 'grace')
    # TODO: maybe replace with logic to move marktools.Articulation
    #new_leaf.articulations[:] = []
    marktools.detach_marks_attached_to_component(new_leaf) 
    contexttools.detach_context_marks_attached_to_component(new_leaf,
        klasses=(contexttools.DynamicMark, ))
    #leaf.after_grace[:] = []
    if hasattr(leaf, 'after_grace'):
        delattr(leaf, '_after_grace')
        delattr(leaf, 'after_grace')

    left_leaf_list = leaftools.set_preprolated_leaf_duration(leaf, unprolated_offset)
    right_leaf_list = leaftools.set_preprolated_leaf_duration(
        new_leaf, leaf_multiplied_duration - unprolated_offset)

    leaf_left_of_split = left_leaf_list[-1]
    leaf_right_of_split = right_leaf_list[0]

    if fracture_spanners:
        spannertools.fracture_spanners_attached_to_component(leaf_left_of_split, direction=Right)

    if tie_after:
        tietools.apply_tie_spanner_to_leaf_pair(leaf_left_of_split, leaf_right_of_split)

    return left_leaf_list, right_leaf_list
