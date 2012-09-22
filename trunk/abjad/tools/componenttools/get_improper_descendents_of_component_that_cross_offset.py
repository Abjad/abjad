from abjad.tools import durationtools


def get_improper_descendents_of_component_that_cross_offset(component, prolated_offset):
    r'''.. versionadded:: 2.0

    Get improper contents of `component` that cross `prolated_offset`::

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

    Examples refer to the score above.

    No components cross prolated offset ``0``::

        >>> componenttools.get_improper_descendents_of_component_that_cross_offset(staff, 0)
        []

    Staff, measure and leaf cross prolated offset ``1/16``::

        >>> componenttools.get_improper_descendents_of_component_that_cross_offset(
        ...     staff, Duration(1, 16))
        [Staff{2}, Measure(2/8, [c'8, d'8]), Note("c'8")]

    Staff and measure cross prolated offset ``1/8``::

        >>> componenttools.get_improper_descendents_of_component_that_cross_offset(
        ...     staff, Duration(1, 8))
        [Staff{2}, Measure(2/8, [c'8, d'8])]

    Staff crosses prolated offset ``1/4``::

        >>> componenttools.get_improper_descendents_of_component_that_cross_offset(
        ...     staff, Duration(1, 4))
        [Staff{2}]

    No components cross prolated offset ``99``::

        >>> componenttools.get_improper_descendents_of_component_that_cross_offset(
        ...     staff, 99)
        []

    Return list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools

    assert isinstance(component, componenttools.Component)
    assert isinstance(prolated_offset, (int, float, durationtools.Duration))

    result = []

    if component.prolated_duration <= prolated_offset:
        return result

    boundary_time = component.start_offset + prolated_offset

    for x in iterationtools.iterate_components_in_expr(component):
        x_start = x.start_offset
        x_stop = x.stop_offset
        if x_start < boundary_time < x_stop:
            result.append(x)

    return result
