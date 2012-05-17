from abjad.tools import durationtools


def update_offset_values_of_component_in_seconds(component):
    r'''.. versionadded:: 2.9

    Update offset values of `component` in seconds.
    '''
    from abjad.tools import componenttools
    try:
        cur_duration_in_seconds = component.duration_in_seconds
        prev = componenttools.get_nth_component_in_time_order_from_component(component, -1)
        if prev is not None:
            component._offset._start_in_seconds = prev._offset._stop_in_seconds
        else:
            component._offset._start_in_seconds = durationtools.Offset(0)
        # this one case is possible for containers only
        if component._offset._start_in_seconds is None:
            raise MissingTempoError
        component._offset._stop_in_seconds = component._offset._start_in_seconds + cur_duration_in_seconds
    except MissingTempoError:
        pass
