from abjad.tools import durationtools


# TODO: implement corresponding function to rest left half
def split_leaf_at_offset_and_rest_right_half(leaf, prolated_duration):
    r'''.. versionadded:: 1.1

    Split `leaf` at `prolated_duration` and rest right half::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> spannertools.SlurSpanner(t[:])
        SlurSpanner(c'8, d'8, e'8, f'8)
        >>> f(t)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> leaftools.split_leaf_at_offset_and_rest_right_half(t.leaves[1], (1, 32))
        ([Note("d'32")], [Note("d'16.")])

    ::

        >>> f(t)
        \new Staff {
            c'8 (
            d'32
            r16.
            e'8
            f'8 )
        }

    Return list of leaves to left of `prolated_duration`
    together with list of leaves to right of `prolated_duration`.

    .. versionchanged:: 2.0
        renamed ``leaftools.shorten()`` to
        ``leaftools.split_leaf_at_offset_and_rest_right_half()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import resttools

    prolated_duration = durationtools.Duration(prolated_duration)

    left, right = componenttools.split_component_at_offset(
        leaf, prolated_duration, fracture_spanners=False)
    for leaf in right:
        rest = resttools.Rest(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [rest])

    return left, right
