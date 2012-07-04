from abjad.tools.componenttools._split_components_by_prolated_durations import _split_components_by_prolated_durations


def split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
    components, durations, tie_after=False):
    r'''.. versionadded:: 1.1

    Partition `components` cyclically by prolated `durations` and do not fracture spanners::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> durations = [Duration(3, 32)]
        >>> componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        ... staff.leaves, durations)
        [[Note("c'16.")], [Note("c'32"), Note("d'16")],
        [Note("d'16"), Note("e'32")], [Note("e'16.")], [Note("f'16.")], [Note("f'32")]]

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'16. [ (
                c'32
                d'16
                d'16 ]
            }
            {
                e'32 [
                e'16.
                f'16.
                f'32 ] )
            }
        }

    Return list of partitioned components.
    '''

    return _split_components_by_prolated_durations(components, durations,
        spanners='unfractured', cyclic=True, tie_after=tie_after)
