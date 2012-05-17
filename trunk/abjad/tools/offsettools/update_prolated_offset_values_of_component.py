from abjad.tools import durationtools


def update_prolated_offset_values_of_component(component):
    r'''.. versionadded:: 2.9

    Update prolated offset values of `component`.
    '''
    from abjad.tools import componenttools
    prev = componenttools.get_nth_component_in_time_order_from_component(component, -1)
    if prev is not None:
        component._offset._start = prev._offset._stop
    else:
        component._offset._start = durationtools.Offset(0)
    component._offset._stop = component._offset._start + component.prolated_duration
