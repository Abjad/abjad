from abjad.tools.componenttools._split_components_by_prolated_durations import _split_components_by_prolated_durations


def split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(
    components, durations, tie_after = False):
    r'''.. versionadded:: 1.1

    Split `components` once by prolated `durations` and do not fracture crossing spanners::

        abjad> t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
        abjad> spannertools.BeamSpanner(t[0])
        BeamSpanner({c'8, d'8})
        abjad> spannertools.BeamSpanner(t[1])
        BeamSpanner({e'8, f'8})
        abjad> spannertools.SlurSpanner(t.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)
        abjad> f(t)
        \new Staff {
            {
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        abjad> durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
        abjad> parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:1], durations)

        abjad> f(t)
        \new Staff {
            {
                c'32 [ (
            }
            {
                c'16.
            }
            {
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    .. versionchanged:: 2.0
        renamed ``partition.unfractured_by_durations()`` to
        ``componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners()``.
    '''

    return _split_components_by_prolated_durations(components, durations,
        spanners = 'unfractured', tie_after = tie_after)
