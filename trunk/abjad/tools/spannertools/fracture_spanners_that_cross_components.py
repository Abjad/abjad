# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def fracture_spanners_that_cross_components(components):
    r'''Fracture to the left of the leftmost component.
    Fracture to the right of the rightmost component.
    Do not fracture spanners of any components at higher levels of score.
    Do not fracture spanners of any components at lower levels of score.
    Return components.

    Components must be logical-voice-contiguous.

    Some spanners may copy during fracture.

    This helper is public-safe.

    ..  container:: example

        **Example:**

        ::

            >>> container = Container(Container(notetools.make_repeated_notes(2)) * 3)
            >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
            ...     container)
            >>> crescendo = spannertools.CrescendoSpanner(container)
            >>> beam = spannertools.BeamSpanner(container[:])
            >>> trill = spannertools.TrillSpanner(container.select_leaves())
            >>> show(conatiner) # doctest: +SKIP

        ..  doctest::

            >>> f(container)
            {
                {
                    c'8 [ \< \startTrillSpan
                    d'8
                }
                {
                    e'8
                    f'8
                }
                {
                    g'8
                    a'8 ] \! \stopTrillSpan
                }
            }

        ::

            >>> spannertools.fracture_spanners_that_cross_components(
            ...     container[1:2])
            SliceSelection({e'8, f'8},)
            >>> show(container) # doctest: +SKIP

        ::

            >>> f(container)
            {
                {
                    c'8 [ \< \startTrillSpan
                    d'8 ]
                }
                {
                    e'8 [
                    f'8 ]
                }
                {
                    g'8 [
                    a'8 ] \! \stopTrillSpan
                }
            }

    Return selection.
    '''
    from abjad.tools import spannertools

    assert componenttools.all_are_contiguous_components_in_same_logical_voice(
        components)

    if 0 < len(components):

        leftmost_component = components[0]
        spannertools.fracture_spanners_attached_to_component(leftmost_component, direction=Left)

        rightmost_component = components[-1]
        spannertools.fracture_spanners_attached_to_component(rightmost_component, direction=Right)

    return components
