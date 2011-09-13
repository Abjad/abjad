from abjad.tools.durationtools import Duration


# TODO: implement corresponding function to rest left half
def split_leaf_at_prolated_duration_and_rest_right_half(leaf, prolated_duration):
    r'''.. versionadded:: 1.1

    Split `leaf` at `prolated_duration` and rest right half::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.SlurSpanner(t[:])
        SlurSpanner(c'8, d'8, e'8, f'8)
        abjad> f(t)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> leaftools.split_leaf_at_prolated_duration_and_rest_right_half(t.leaves[1], (1, 32))
        ([Note("d'32")], [Note("d'16.")])

    ::

        abjad> f(t)
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
        ``leaftools.split_leaf_at_prolated_duration_and_rest_right_half()``.
    '''
    from abjad.tools.resttools.Rest import Rest
    from abjad.tools.componenttools.move_parentage_and_spanners_from_components_to_components import move_parentage_and_spanners_from_components_to_components
    from abjad.tools.componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners import split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners

    prolated_duration = Duration(prolated_duration)

    left, right = split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(
        leaf, prolated_duration)
    for leaf in right:
        rest = Rest(leaf)
        move_parentage_and_spanners_from_components_to_components([leaf], [rest])

    return left, right
