# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import durationtools


def rest_leaf_at_offset(leaf, offset):
    r'''Split `leaf` at `offset` and rest right half:

    ::

        >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> leaftools.rest_leaf_at_offset(staff.select_leaves()[1], (1, 32))
        (Selection(Note("d'32"),), Selection(Note("d'16."),))

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'32
            r16.
            e'8
            f'8 )
        }

    Returns pair of selections.
    '''
    from abjad.tools import resttools

    offset = durationtools.Offset(offset)

    left, right = componenttools.split(
        [leaf], 
        [offset], 
        fracture_spanners=False, 
        tie_split_notes=False,
        )

    for leaf in right:
        rest = resttools.Rest(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components(
            [leaf], [rest])

    return left, right
