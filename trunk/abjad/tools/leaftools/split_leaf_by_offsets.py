import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import pitchtools


def split_leaf_by_offsets(leaf, offsets, cyclic=False, tie_pitch_carrier=True, tie_nonpitch_carrier=False):
    r'''.. versionadded:: 2.10

    Split `leaf` by `offsets`.

    Example 1. Split note once by `offsets` and tie split notes::

        >>> staff = Staff("c'1 ( d'1 )")

    ::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_by_offsets(staff[0], [(3, 8)], tie_pitch_carrier=True)
        [[Note("c'4.")], [Note("c'2"), Note("c'8")]]

    ::

        >>> f(staff)
        \new Staff {
            c'4. ( ~
            c'2 ~
            c'8
            d'1 )
        }

    Example 2. Split note cyclically by `offsets` and tie split notes::

        >>> staff = Staff("c'1 ( d'1 )")

    ::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_by_offsets(staff[0], [(3, 8)], cyclic=True, tie_pitch_carrier=True)
        [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]

    ::

        >>> f(staff)
        \new Staff {
            c'4. ( ~
            c'4. ~
            c'4
            d'1 )
        }

    Example 3. Split note once by `offsets` and do no tie split notes::

        >>> staff = Staff("c'1 ( d'1 )")

    ::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_by_offsets(staff[0], [(3, 8)], tie_pitch_carrier=False)
        [[Note("c'4.")], [Note("c'2"), Note("c'8")]]

    ::

        >>> f(staff)
        \new Staff {
            c'4. (
            c'2 ~
            c'8
            d'1 )
        }

    Example 4. Split note cyclically by `offsets` and do not tie split notes::

        >>> staff = Staff("c'1 ( d'1 )")

    ::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_by_offsets(staff[0], [(3, 8)], cyclic=True, tie_pitch_carrier=False)
        [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]

    ::

        >>> f(staff)
        \new Staff {
            c'4. (
            c'4.
            c'4
            d'1 )
        }

    Return list of shards.
    '''
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    from abjad.tools import tietools
    
    assert isinstance(leaf, leaftools.Leaf) 
    offsets = [durationtools.Offset(offset) for offset in offsets]

    if cyclic:
        offsets = sequencetools.repeat_sequence_to_weight_exactly(offsets, leaf.written_duration)

    durations = [durationtools.Duration(offset) for offset in offsets]

    if sum(durations) < leaf.written_duration:
        last_duration = leaf.written_duration - sum(durations)
        durations.append(last_duration) 

    sequencetools.truncate_sequence_to_weight(durations, leaf.written_duration)

    result = []
    leaf_copy = copy.deepcopy(leaf)
    for duration in durations:
        new_leaf = copy.deepcopy(leaf)
        shard = leaftools.set_preprolated_leaf_duration(new_leaf, duration)
        result.append(shard)

    flattened_result = sequencetools.flatten_sequence(result)

    if  (pitchtools.is_pitch_carrier(leaf) and tie_pitch_carrier) or \
        (not pitchtools.is_pitch_carrier(leaf) and tie_nonpitch_carrier):
        tietools.remove_tie_spanners_from_components_in_expr(flattened_result)
        tietools.TieSpanner(flattened_result)
     
    componenttools.move_parentage_and_spanners_from_components_to_components([leaf], flattened_result)

    return result
