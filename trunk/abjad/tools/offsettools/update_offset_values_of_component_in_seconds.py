# -*- encoding: utf-8 -*-
from abjad.tools import durationtools


def update_offset_values_of_component_in_seconds(component):
    r'''Update offset values of `component` in seconds.
    '''
    from abjad.tools import componenttools
    try:
        current_duration_in_seconds = component.get_duration(in_seconds=True)
        prev = componenttools.get_nth_component_in_time_order_from_component(
            component, -1)
        if prev is not None:
            component._start_offset_in_seconds = \
                prev._get_timespan(in_seconds=True).stop_offset
        else:
            component._start_offset_in_seconds = durationtools.Offset(0)
        # this one case is possible for containers only
        if component._start_offset_in_seconds is None:
            raise MissingTempoError
        component._stop_offset_in_seconds = \
            component._start_offset_in_seconds + current_duration_in_seconds
    except MissingTempoError:
        pass
