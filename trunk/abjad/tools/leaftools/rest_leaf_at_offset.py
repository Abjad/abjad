from abjad.tools import componenttools
from abjad.tools import durationtools


# TODO: implement corresponding function to rest left half
def rest_leaf_at_offset(leaf, offset):
    r'''.. versionadded:: 1.1

    Split `leaf` at `offset` and rest right half::

        >>> staff = Staff("c'8 ( d'8 e'8 f'8 )")

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> leaftools.rest_leaf_at_offset(staff.leaves[1], (1, 32))
        ([Note("d'32")], [Note("d'16.")])

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'32
            r16.
            e'8
            f'8 )
        }

    Return list of leaves to left of `offset`
    together with list of leaves to right of `offset`.

    .. versionchanged:: 2.0
        renamed ``leaftools.shorten()`` to
        ``leaftools.rest_leaf_at_offset()``.
    '''
    from abjad.tools import resttools

    offset = durationtools.Offset(offset)

    left, right = componenttools.split_component_at_offset(
        leaf, offset, fracture_spanners=False, tie_split_notes=False)

    for leaf in right:
        rest = resttools.Rest(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [rest])

    return left, right
