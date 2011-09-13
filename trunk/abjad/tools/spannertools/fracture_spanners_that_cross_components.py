from abjad.tools.spannertools.fracture_all_spanners_attached_to_component import fracture_all_spanners_attached_to_component


def fracture_spanners_that_cross_components(components):
    r'''Fracture to the left of the leftmost component.
    Fracture to the right of the rightmost component.
    Do not fracture spanners of any components at higher levels of score.
    Do not fracture spanners of any components at lower levels of score.
    Return components.

    Components must be thread-contiguous.
    Some spanners may copy during fracture.
    This helper is public-safe.

    Example::

        t = Staff(Container(notetools.make_repeated_notes(2)) * 3)
        pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
        spannertools.CrescendoSpanner(t)
        spannertools.BeamSpanner(t[:])
        spannertools.TrillSpanner(t.leaves)

        \new Staff {
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
            }   }

        spannertools.fracture_spanners_that_cross_components(t[1:2])

        \new Staff {
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

    .. versionchanged:: 2.0
        renamed ``spannertools.fracture_crossing()`` to
        ``spannertools.fracture_spanners_that_cross_components()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    if 0 < len(components):

        leftmost_component = components[0]
        #leftmost_component.spanners.fracture(direction = 'left')
        fracture_all_spanners_attached_to_component(leftmost_component, direction = 'left')

        rightmost_component = components[-1]
        #rightmost_component.spanners.fracture(direction = 'right')
        fracture_all_spanners_attached_to_component(rightmost_component, direction = 'right')

    return components
