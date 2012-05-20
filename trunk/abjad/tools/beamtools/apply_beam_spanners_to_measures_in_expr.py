from abjad.tools import measuretools
from abjad.tools.beamtools import BeamSpanner


def apply_beam_spanners_to_measures_in_expr(expr):
    r'''.. versionadded:: 1.1

    Apply beam spanners to measures in `expr`::

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

        abjad> beamtools.apply_beam_spanners_to_measures_in_expr(staff)
        [BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|)]

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [
                d'8 ]
            }
            {
                e'8 [
                f'8 ]
            }
        }

    Return list of beams created.

    .. versionchanged:: 2.0
        renamed ``measuretools.beam()`` to
        ``beamtools.apply_beam_spanners_to_measures_in_expr()``.

    .. versionchanged:: 2.9
        renamed ``measuretools.apply_beam_spanners_to_measures_in_expr()`` to
        ``beamtools.apply_beam_spanners_to_measures_in_expr()``.
    '''
    from abjad.tools import beamtools

    # init beams created
    beams_created = []

    # apply beam spanners to measures in expr
    for measure in measuretools.iterate_measures_forward_in_expr(expr):
        beam = beamtools.apply_beam_spanner_to_measure(measure)
        beams_created.append(beam)

    # return beams created
    return beams_created
