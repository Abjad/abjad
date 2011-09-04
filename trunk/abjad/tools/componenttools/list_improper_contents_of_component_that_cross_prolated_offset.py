from abjad.tools.componenttools._Component import _Component
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr
from abjad.tools import durationtools


def list_improper_contents_of_component_that_cross_prolated_offset(component, prolated_offset):
    r'''.. versionadded:: 2.0

    List improper contents of `component` that cross `prolated_offset`::

        abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
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

    Examples refer to the score above.

    No components cross prolated offset ``0``::

        abjad> componenttools.list_improper_contents_of_component_that_cross_prolated_offset(staff, 0)
        []

    Staff, measure and leaf cross prolated offset ``1/16``::

        abjad> componenttools.list_improper_contents_of_component_that_cross_prolated_offset(staff, Duration(1, 16))
        [Staff{2}, Measure(2/8, [c'8, d'8]), Note("c'8")]

    Staff and measure cross prolated offset ``1/8``::

        abjad> componenttools.list_improper_contents_of_component_that_cross_prolated_offset(staff, Duration(1, 8))
        [Staff{2}, Measure(2/8, [c'8, d'8])]

    Staff crosses prolated offset ``1/4``::

        abjad> componenttools.list_improper_contents_of_component_that_cross_prolated_offset(staff, Duration(1, 4))
        [Staff{2}]

    No components cross prolated offset ``99``::

        abjad> componenttools.list_improper_contents_of_component_that_cross_prolated_offset(staff, 99)
        []

    Return list.
    '''

    assert isinstance(component, _Component)
    assert isinstance(prolated_offset, (int, float, durationtools.Duration))

    result = []

    if component.prolated_duration <= prolated_offset:
        return result

    boundary_time = component._offset.start + prolated_offset

    for x in iterate_components_forward_in_expr(component, _Component):
        x_start = x._offset.start
        x_stop = x._offset.stop
        if x_start < boundary_time < x_stop:
            result.append(x)

    return result
