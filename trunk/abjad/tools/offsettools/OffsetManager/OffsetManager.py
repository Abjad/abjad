from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class OffsetManager(AbjadObject):
    '''Update start and stop offsets of all components in score.
    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def update_offset_values_of_component(component):
        r'''Update prolated offset values of `component`.
        '''
        from abjad.tools import componenttools
        prev = componenttools.get_nth_component_in_time_order_from_component(
            component, -1)
        if prev is not None:
            start_offset = prev._stop_offset
        else:
            start_offset = durationtools.Offset(0)
        stop_offset = start_offset + component._get_duration()
        component._start_offset = start_offset
        component._stop_offset = stop_offset
        component._timespan._start_offset = start_offset
        component._timespan._stop_offset = stop_offset

    @staticmethod
    def update_offset_values_of_component_in_seconds(component):
        r'''Update offset values of `component` in seconds.
        '''
        from abjad.tools import componenttools
        try:
            current_duration_in_seconds = \
                component._get_duration(in_seconds=True)
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
