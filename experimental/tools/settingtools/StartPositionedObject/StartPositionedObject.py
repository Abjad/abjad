import abc
import numbers
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StartPositionedObject(AbjadObject):
    '''Start-positioned object.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, start_offset=None):
        start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        if hasattr(self.payload, 'duration'):
            return self.payload.duration
        else:
            return self._get_duration_of_list(self.payload)

    @property
    def _stop_offset(self):
        return self._start_offset + self._duration

    ### PRIVATE METHODS ###

    def _get_duration_of_expr(self, expr):
        if hasattr(expr, 'duration'):
            return expr.duration
        elif hasattr(expr, 'prolated_duration'):
            return expr.prolated_duration
        elif isinstance(expr, numbers.Number):
            return durationtools.Duration(expr)
        else:
            return durationtools.Duration(expr)

    def _get_duration_of_list(self, expr):
        duration = durationtools.Duration(0)
        for element in expr:
            duration += self._get_duration_of_expr(element)
        return duration

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Start-positioned object start offset.
    
        Return offset.
        '''
        return self.timespan.start_offset

    # TODO: Maybe implement not on start-positioned expressions.
    #       Maybe implement only on start-positioned products.
    @property
    def stop_offset(self):
        '''Start-positioned object stop offset.

        Return offset.
        '''
        return self.timespan.stop_offset

    # TODO: Maybe implement not on start-positioned expressions.
    #       Maybe implement only on start-positioned products.
    @property
    def timespan(self):
        '''Start-positioned object timespan.

        Return timespan.
        '''
        return timespantools.Timespan(self._start_offset, self._stop_offset)
