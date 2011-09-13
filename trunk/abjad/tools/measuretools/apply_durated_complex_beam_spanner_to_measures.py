from abjad.tools.spannertools import DuratedComplexBeamSpanner


def apply_durated_complex_beam_spanner_to_measures(measures):
    r'''.. versionadded:: 1.1

    Apply durated complex beam spanner to `measures`::

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
                \time 2/8
                e'8
                f'8
            }
        }

    ::

        abjad> measures = staff[:]
        abjad> measuretools.apply_durated_complex_beam_spanner_to_measures(measures)
        DuratedComplexBeamSpanner(|2/8(2)|, |2/8(2)|)

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #1
                c'8 [
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #1
                d'8
            }
            {
                \time 2/8
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #1
                e'8
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #0
                f'8 ]
            }
        }

    Set beam spanner durations to preprolated measure durations.

    Return beam spanner created.

    .. versionchanged:: 2.0
        renamed ``measuretools.beam_together()``.
    '''
    from abjad.tools import spannertools

    durations = []
    for measure in measures:
        #measure.beam.unspan()
        spannertools.destroy_all_spanners_attached_to_component(measure, spannertools.BeamSpanner)
        durations.append(measure.preprolated_duration)
    beam = DuratedComplexBeamSpanner(measures, durations = durations, span = 1)
    return beam
