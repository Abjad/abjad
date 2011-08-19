from abjad.tools.componenttools._split_components_by_prolated_durations import _split_components_by_prolated_durations


def split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners(
    components, durations, tie_after = False):
    r'''.. versionadded:: 1.1

    Partition `components` cyclically by prolated `durations` and fracture spanners::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> spannertools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        abjad> spannertools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        abjad> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)
        abjad> f(staff)
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

        abjad> durations = [Duration(3, 32)]
        abjad> componenttools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners(staff.leaves, durations)
        [[Note("c'16.")], [Note("c'32"), Note("d'16")], [Note("d'16"), Note("e'32")],
        [Note("e'16.")], [Note("f'16.")], [Note("f'32")]]

    ::

        abjad> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16. ( ) [
                c'32 (
                d'16 )
                d'16 ] (
            }
            {
                \time 2/8
                e'32 ) [
                e'16. (
                f'16. )
                f'32 ] ( )
            }
        }

    Return list of partitioned components.

    .. versionchanged:: 2.0
        renamed ``partition.cyclic_fractured_by_durations()`` to
        ``componenttools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners()``.
    '''

    return _split_components_by_prolated_durations(components, durations,
        spanners = 'fractured', cyclic = True, tie_after = tie_after)
