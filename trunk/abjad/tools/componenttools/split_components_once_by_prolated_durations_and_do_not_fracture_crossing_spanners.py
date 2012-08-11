from abjad.tools.componenttools.split_components_by_prolated_durations import split_components_by_prolated_durations


def split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(
    components, durations, tie_after=False):
    r'''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.split_components_by_durations()`` instead.

    Split `components` once by prolated `durations` and do not fracture crossing spanners::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")

    ::

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

        >>> durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
        >>> parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        ... staff[:1], durations)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 1/32
                c'32 [ (
            }
            {
                \time 3/32
                c'16.
            }
            {
                \time 4/32
                d'8 ]
            }
            {
                \time 2/8
                e'8 [
                f'8 ] )
            }
        }

    .. versionchanged:: 2.0
        renamed ``partition.unfractured_by_durations()`` to
        ``componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners()``.
    '''

    return split_components_by_prolated_durations(components, durations,
        fracture_spanners=False, tie_after=tie_after)
