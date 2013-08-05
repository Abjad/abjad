# -*- encoding: utf-8 -*-
import copy
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import pitchtools


def split_leaf_at_offsets(
    leaf,
    offsets,
    cyclic=False,
    fracture_spanners=False,
    tie_split_notes=True,
    tie_split_rests=False,
    ):
    r'''Split `leaf` at `offsets`.

    Example 1. Split note once at `offsets` and tie split notes:

    ::

        >>> staff = Staff("c'1 ( d'1 )")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_at_offsets(staff[0], [(3, 8)],
        ...     tie_split_notes=True)
        [[Note("c'4.")], [Note("c'2"), Note("c'8")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4. ( ~
            c'2 ~
            c'8
            d'1 )
        }

    Example 2. Split note cyclically at `offsets` and tie split notes:

    ::

        >>> staff = Staff("c'1 ( d'1 )")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_at_offsets(staff[0], [(3, 8)], cyclic=True,
        ...     tie_split_notes=True)
        [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4. ( ~
            c'4. ~
            c'4
            d'1 )
        }

    Example 3. Split note once at `offsets` and do no tie split notes:

    ::

        >>> staff = Staff("c'1 ( d'1 )")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_at_offsets(staff[0], [(3, 8)],
        ...     tie_split_notes=False)
        [[Note("c'4.")], [Note("c'2"), Note("c'8")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4. (
            c'2 ~
            c'8
            d'1 )
        }

    Example 4. Split note cyclically at `offsets` and do not tie split notes:

    ::

        >>> staff = Staff("c'1 ( d'1 )")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'1 (
            d'1 )
        }

    ::

        >>> leaftools.split_leaf_at_offsets(staff[0], [(3, 8)], cyclic=True,
        ...     tie_split_notes=False)
        [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4. (
            c'4.
            c'4
            d'1 )
        }

    Example 5. Split tupletted note once at `offsets` and tie split notes:

    ::

        >>> staff = Staff(r"\times 2/3 { c'2 ( d'2 e'2 ) }")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'2 (
                d'2
                e'2 )
            }
        }

    ::

        >>> leaftools.split_leaf_at_offsets(staff.select_leaves()[1], [(1, 6)], cyclic=False,
        ...     tie_split_notes=True)
        [[Note("d'4")], [Note("d'4")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'2 (
                d'4 ~
                d'4
                e'2 )
            }
        }

    .. note:: Add examples showing mark and context mark handling.

    Return list of shards.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import marktools
    from abjad.tools import selectiontools
    from abjad.tools import spannertools

    assert isinstance(leaf, leaftools.Leaf)
    offsets = [durationtools.Offset(offset) for offset in offsets]

    if cyclic:
        offsets = sequencetools.repeat_sequence_to_weight_exactly(
            offsets, leaf.get_duration())

    durations = [durationtools.Duration(offset) for offset in offsets]

    if sum(durations) < leaf.get_duration():
        last_duration = leaf.get_duration() - sum(durations)
        durations.append(last_duration)

    sequencetools.truncate_sequence_to_weight(durations, leaf.get_duration())

    result = []
    leaf_prolation = leaf.select_parentage(include_self=False).prolation
    leaf_copy = componenttools.copy_components_and_detach_spanners([leaf])[0]
    for duration in durations:
        new_leaf = \
            componenttools.copy_components_and_detach_spanners([leaf])[0]
        preprolated_duration = duration / leaf_prolation
        shard = leaftools.set_preprolated_leaf_duration(
            new_leaf, preprolated_duration)
        shard = [x.select_parentage().root for x in shard]
        result.append(shard)

    flattened_result = sequencetools.flatten_sequence(result)
    flattened_result = selectiontools.SliceSelection(flattened_result)
    spanner_classes = (spannertools.TieSpanner,)
    if spannertools.get_spanners_attached_to_any_improper_parent_of_component(
        leaf, spanner_classes=spanner_classes):
        selection = selectiontools.select(flattened_result)
        selection.detach_spanners(spanner_classes=spanner_classes)
    componenttools.move_parentage_and_spanners_from_components_to_components(
        [leaf], flattened_result)

    if fracture_spanners:
        first_shard = result[0]
        spannertools.fracture_spanners_attached_to_component(
            first_shard[-1], direction=Right)
        last_shard = result[-1]
        spannertools.fracture_spanners_attached_to_component(
            last_shard[0], direction=Left)
        for middle_shard in result[1:-1]:
            spannertools.fracture_spanners_attached_to_component(
                middle_shard[0], direction=Left)
            spannertools.fracture_spanners_attached_to_component(
                middle_shard[-1], direction=Right)

    # adjust first leaf
    first_leaf = flattened_result[0]
    leaf.detach_grace_containers(kind='after')

    # adjust any middle leaves
    for middle_leaf in flattened_result[1:-1]:
        middle_leaf.detach_grace_containers(kind='grace')
        leaf.detach_grace_containers(kind='after')
        middle_leaf.select().detach_marks()
        middle_leaf.select().detach_marks(contexttools.ContextMark)

    # adjust last leaf
    last_leaf = flattened_result[-1]
    last_leaf.detach_grace_containers(kind='grace')
    last_leaf.select().detach_marks()
    last_leaf.select().detach_marks(contexttools.ContextMark)

    # tie split notes, rests and chords as specified
    if  (pitchtools.is_pitch_carrier(leaf) and tie_split_notes) or \
        (not pitchtools.is_pitch_carrier(leaf) and tie_split_rests):
        flattened_result_leaves = iterationtools.iterate_leaves_in_expr(
            flattened_result)
        # TODO: implement SliceSelection._attach_tie_spanner_to_leaves()
        for leaf_pair in sequencetools.iterate_sequence_pairwise_strict(
            flattened_result_leaves):
            selection = selectiontools.SequentialLeafSelection(leaf_pair)
            selection._attach_tie_spanner_to_leaf_pair()

    # return result
    return result
