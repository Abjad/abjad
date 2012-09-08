from abjad.tools import durationtools
from experimental.timespaninequalitytools.Timespan import Timespan



class TimespanConstant(Timespan):
    r'''.. versionadded:: 1.0

    Timespan constant.

    ::

        >>> from experimental import *

    Timespan contant ``[1/2, 3/2)``::

        >>> timespan_constant = timespaninequalitytools.TimespanConstant((1, 2), (3, 2)) 

    ::

        >>> timespan_constant
        TimespanConstant(start_offset=Offset(1, 2), stop_offset=Offset(3, 2))

    ::
    
        >>> z(timespan_constant)
        timespaninequalitytools.TimespanConstant(
            start_offset=durationtools.Offset(1, 2),
            stop_offset=durationtools.Offset(3, 2)
            )

    Timespan constants are object-modeled offset pairs.

    Timespan constants are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None):
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self.stop_offset - self.start_offset

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def stop_offset(self):
        return self._stop_offset
