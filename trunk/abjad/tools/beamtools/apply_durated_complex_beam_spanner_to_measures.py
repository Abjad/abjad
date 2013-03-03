from abjad.tools import spannertools


def apply_durated_complex_beam_spanner_to_measures(measures):
    r'''.. versionadded:: 1.1

    Apply durated complex beam spanner to `measures`::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
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

        >>> show(staff) # doctest: +SKIP

    ::

        >>> measures = staff[:]
        >>> beamtools.apply_durated_complex_beam_spanner_to_measures(measures)
        DuratedComplexBeamSpanner(|2/8(2)|, |2/8(2)|)

    ::

        >>> f(staff)
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
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #1
                e'8
                \set stemLeftBeamCount = #1
                \set stemRightBeamCount = #0
                f'8 ]
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Set beam spanner durations to preprolated measure durations.

    Return beam spanner created.
    '''
    from abjad.tools import beamtools

    durations = []
    for measure in measures:
        spannertools.destroy_spanners_attached_to_component(measure, beamtools.BeamSpanner)
        durations.append(measure.preprolated_duration)
    beam = beamtools.DuratedComplexBeamSpanner(measures, durations=durations, span=1)
    return beam
