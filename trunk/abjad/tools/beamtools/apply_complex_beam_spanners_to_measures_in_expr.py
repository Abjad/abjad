from abjad.tools import measuretools


def apply_complex_beam_spanners_to_measures_in_expr(expr):
    r'''.. versionadded:: 2.0

    Apply complex beam spanners to measures in `expr`::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }

    ::

        abjad> beamtools.apply_complex_beam_spanners_to_measures_in_expr(staff)
        [ComplexBeamSpanner(|2/8(2)|), ComplexBeamSpanner(|2/8(2)|)]

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #1
                c'8 [
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #0
                d'8 ]
            }
            {
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #1
                e'8 [
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #0
                f'8 ]
            }
        }


    Return list of beams created.

    .. versionchanged:: 2.9
        renamed ``measuretools.apply_complex_beam_spanners_to_measures_in_expr()`` to
        ``beamtools.apply_complex_beam_spanners_to_measures_in_expr()``.
    '''
    from abjad.tools import beamtools

    # init beams created
    beams_created = []

    # apply complex beam spanners to measures in expr
    for measure in measuretools.iterate_measures_forward_in_expr(expr):
        beam = beamtools.ComplexBeamSpanner(measure)
        beams_created.append(beam)

    # return beams created
    return beams_created
