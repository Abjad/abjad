# -*- encoding: utf-8 -*-
import copy
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import pitchtools


# TODO: This should be replaced in favor of leaftools.split_leaf_at_offsets().
#       The precondition is that leaftools.split_leaf_at_offsets() must be
#       extended to handle graces.
#       Also important to migrate over the (large-ish) set of tests for this
#       function.
def split_leaf_at_offset(
    leaf, 
    offset, 
    fracture_spanners=False,
    tie_split_notes=True, 
    tie_split_rests=False,
    ):
    r'''Splits `leaf` at `offset`.

    ..  container:: example
    
        **Example 1.** Split note at assignable offset. Two notes result. 
        Do not tie notes:

        ::

            >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
            >>> select(staff[:]).attach_spanners(spannertools.BeamSpanner)
            (BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|))
            >>> contexttools.DynamicMark('f')(staff.select_leaves()[0])
            DynamicMark('f')(c'8)
            >>> marktools.Articulation('accent')(staff.select_leaves()[0])
            Articulation('accent')(c'8)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

            >>> leaftools.split_leaf_at_offset(
            ...     staff.select_leaves()[0], 
            ...     (1, 32),
            ...     tie_split_notes=False,
            ...     )
            ([Note("c'32")], [Note("c'16.")])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

    ..  container:: example
    
        **Example 2.** Handle grace and after grace containers correctly.

        ::

            >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
            >>> select(staff[:]).attach_spanners(spannertools.BeamSpanner)
            (BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|))
            >>> leaftools.GraceContainer("cs'16")(staff.select_leaves()[0])
            Note("c'8")
            >>> leaftools.GraceContainer("ds'16", kind='after')(staff.select_leaves()[0])
            Note("c'8")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    \grace {
                        cs'16
                    }
                    \afterGrace
                    c'8 [ (
                    {
                        ds'16
                    }
                    d'8 ]
                }
                {
                    e'8 [
                    f'8 ] )
                }
            }

        ::

            >>> leaftools.split_leaf_at_offset(
            ...     staff.select_leaves()[0], 
            ...     (1, 32),
            ...     tie_split_notes=False,
            ...     )
            ([Note("c'32")], [Note("c'16.")])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    \grace {
                        cs'16
                    }
                    c'32 [ (
                    \afterGrace
                    c'16.
                    {
                        ds'16
                    }
                    d'8 ]
                }
                {
                    e'8 [
                    f'8 ] )
                }
            }

    Returns pair.
    '''

    return leaf._split_at_offset(
        offset, 
        fracture_spanners=fracture_spanners,
        tie_split_notes=tie_split_notes, 
        tie_split_rests=tie_split_rests,
        )
