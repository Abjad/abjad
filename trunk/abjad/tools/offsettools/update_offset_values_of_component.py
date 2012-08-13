from abjad.tools import durationtools


def update_offset_values_of_component(component):
    r'''.. versionadded:: 2.9

    Update prolated offset values of `component`.
    '''
    from abjad.tools import componenttools
    prev = componenttools.get_nth_component_in_time_order_from_component(component, -1)
    if prev is not None:
        component._start_offset = prev._stop_offset
    else:
        component._start_offset = durationtools.Offset(0)
    component._stop_offset = component._start_offset + component.prolated_duration
