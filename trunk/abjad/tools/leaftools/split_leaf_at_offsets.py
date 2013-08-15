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
    r'''Splits `leaf` at `offsets`.

    ..  container:: example
    
        **Example 1.** Split note once at `offsets` and tie split notes:

        ::

            >>> staff = Staff("c'1 ( d'1 )")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'1 (
                d'1 )
            }

        ::

            >>> leaftools.split_leaf_at_offsets(
            ...     staff[0], 
            ...     [(3, 8)],
            ...     tie_split_notes=True,
            ...     )
            [[Note("c'4.")], [Note("c'2"), Note("c'8")]]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4. ( ~
                c'2 ~
                c'8
                d'1 )
            }

    ..  container:: example
    
        **Example 2.** Split note cyclically at `offsets` and tie split notes:

        ::

            >>> staff = Staff("c'1 ( d'1 )")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'1 (
                d'1 )
            }

        ::

            >>> leaftools.split_leaf_at_offsets(
            ...     staff[0], 
            ...     [(3, 8)], 
            ...     cyclic=True,
            ...     tie_split_notes=True,
            ...     )
            [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4. ( ~
                c'4. ~
                c'4
                d'1 )
            }

    ..  container:: example
    
        **Example 3.** Split note once at `offsets` and do no tie split notes:

        ::

            >>> staff = Staff("c'1 ( d'1 )")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'1 (
                d'1 )
            }

        ::

            >>> leaftools.split_leaf_at_offsets(
            ...     staff[0], 
            ...     [(3, 8)],
            ...     tie_split_notes=False,
            ...     )
            [[Note("c'4.")], [Note("c'2"), Note("c'8")]]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4. (
                c'2 ~
                c'8
                d'1 )
            }

    ..  container:: example
    
        **Example 4.** Split note cyclically at `offsets` and do not 
        tie split notes:

        ::

            >>> staff = Staff("c'1 ( d'1 )")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'1 (
                d'1 )
            }

        ::

            >>> leaftools.split_leaf_at_offsets(
            ...     staff[0], 
            ...     [(3, 8)], 
            ...     cyclic=True,
            ...     tie_split_notes=False,
            ...     )
            [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4. (
                c'4.
                c'4
                d'1 )
            }

    ..  container:: example
    
        **Example 5.** Split tupletted note once at `offsets` 
        and tie split notes:

        ::

            >>> staff = Staff(r"\times 2/3 { c'2 ( d'2 e'2 ) }")
            >>> show(staff) # doctest: +SKIP

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

            >>> leaftools.split_leaf_at_offsets(
            ...     staff.select_leaves()[1], 
            ...     [(1, 6)], 
            ...     cyclic=False,
            ...     tie_split_notes=True,
            ...     )
            [[Note("d'4")], [Note("d'4")]]
            >>> show(staff) # doctest: +SKIP

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

    Returns list of shards.
    '''

    return leaf._split_at_offsets(
        offsets,
        cyclic=cyclic,
        fracture_spanners=fracture_spanners,
        tie_split_notes=tie_split_notes,
        tie_split_rests=tie_split_rests,
        )
