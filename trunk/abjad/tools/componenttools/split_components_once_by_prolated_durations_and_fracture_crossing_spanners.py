from abjad.tools.componenttools._split_components_by_prolated_durations import _split_components_by_prolated_durations


def split_components_once_by_prolated_durations_and_fracture_crossing_spanners(
    components, durations, tie_after = False):
    r'''.. versionadded:: 1.1

    Split `components` once by prolated `durations` and fracture crossing spanners::

        abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
        abjad> spannertools.BeamSpanner(t[0])
        BeamSpanner(|2/8(2)|)
        abjad> spannertools.BeamSpanner(t[1])
        BeamSpanner(|2/8(2)|)
        abjad> spannertools.SlurSpanner(t.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)
        abjad> f(t)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }

    ::

        abjad> durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
        abjad> parts = componenttools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners(t[:1], durations)
        abjad> f(t)
        \new Staff {
            {
                \time 1/32
                c'32 [ ] ( )
            }
            {
                \time 3/32
                c'16. [ ] ( )
            }
            {
                \time 4/32
                d'8 [ ] (
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }

    .. versionchanged:: 2.0
        renamed ``partition.fractured_by_durations()`` to
        ``componenttools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners()``.
    '''

    return _split_components_by_prolated_durations(components, durations,
        spanners = 'fractured', tie_after = tie_after)
