# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools.handlertools.Handler import Handler


class DynamicHandler(Handler):
    r'''Dynamic handler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_minimum_duration',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, minimum_duration=None):
        Handler.__init__(self)
        if minimum_duration is not None:
            minimum_duration = durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration

    ### PRIVATE METHODS ###

    def _group_contiguous_logical_ties(self, logical_ties):
        result = []
        current_group = [logical_ties[0]]
        for logical_tie in logical_ties[1:]:
            last_timespan = current_group[-1].get_timespan()
            current_timespan = logical_tie.get_timespan()
            if last_timespan.stops_when_timespan_starts(current_timespan):
                current_group.append(logical_tie)
            else:
                result.append(current_group)
                current_group = [logical_tie]
        if current_group:
            result.append(current_group)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of duration handler.

        Returns duration or none.
        '''
        return self._minimum_duration