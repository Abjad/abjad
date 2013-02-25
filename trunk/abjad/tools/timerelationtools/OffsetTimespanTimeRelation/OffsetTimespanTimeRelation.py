import fractions
from abjad.tools import durationtools
from abjad.tools.timerelationtools.TimeRelation import TimeRelation


class OffsetTimespanTimeRelation(TimeRelation):
    r'''.. versionadded:: 2.11

    Offset / timespan time relation:

    ::

        >>> offset = Offset(5)
        >>> timespan = timespantools.Timespan(0, 10)
        >>> time_relation = timerelationtools.offset_happens_during_timespan(
        ...     offset=offset, timespan=timespan, hold=True)

    ::

        >>> z(time_relation)
        timerelationtools.OffsetTimespanTimeRelation(
            'timespan.start <= offset < timespan.stop',
            timespan=timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(10, 1)
                ),
            offset=durationtools.Offset(5, 1)
            )

    Offset / timespan time relations are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, template, timespan=None, offset=None):
        TimeRelation.__init__(self, template)
        self._timespan = timespan
        self._offset = offset

    ### SPECIAL METHODS ###

    def __call__(self, timespan=None, offset=None):
        r'''Evaluate time relation:

            >>> time_relation()
            True

        Raise value error is either `offset` or `timespan` is none.

        Otherwise return boolean.
        '''
        from abjad.tools import timespantools
        if timespan is None:
            timespan = self.timespan
        if offset is None:
            offset = self.offset
        if timespan is None or offset is None:
            raise ValueError('time relation is not fully loaded.')
        timespan = timespantools.Timespan()._get_timespan(timespan)
        offset = durationtools.Offset(offset)
        timespan_start, timespan_stop = self._get_expr_offsets(timespan)
        command = self.template
        command = command.replace('timespan.start', repr(timespan_start))
        command = command.replace('timespan.stop', repr(timespan_stop))
        command = command.replace('offset', repr(offset))
        result = eval(command, {'Offset': durationtools.Offset})
        return result

    def __eq__(self, expr):
        '''True when `expr` equals time relation. Otherwise false:

        ::

            >>> offset = Offset(5)
            >>> time_relation_1 = timerelationtools.offset_happens_during_timespan()
            >>> time_relation_2 = timerelationtools.offset_happens_during_timespan(
            ...     offset=offset)

        ::

            >>> time_relation_1 == time_relation_1
            True
            >>> time_relation_1 == time_relation_2
            False
            >>> time_relation_2 == time_relation_2
            True

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.template == expr.template:
                if self.timespan == expr.timespan:
                    if self.offset == expr.offset:
                        return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_fully_loaded(self):
        '''True when `timespan` and `offset` are both not none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_loaded
            True

        Return boolean.
        '''
        return self.timespan is not None and self.offset is not None

    @property
    def is_fully_unloaded(self):
        '''True when `timespan` and `offset` are both none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_unloaded
            False

        Return boolean.
        '''
        return self.timespan is None and self.offset is None

    @property
    def offset(self):
        '''Time relation offset:

        ::

            >>> time_relation.offset
            Offset(5, 1)

        Return offset or none.
        '''
        return self._offset

    @property
    def storage_format(self):
        '''Time relation storage format:

        ::

            >>> z(time_relation)
            timerelationtools.OffsetTimespanTimeRelation(
                'timespan.start <= offset < timespan.stop',
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                offset=durationtools.Offset(5, 1)
                )

        Return string.
        '''
        return TimeRelation.storage_format.fget(self)

    @property
    def timespan(self):
        '''Time relation timepsan:

        ::

            >>> time_relation.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Return timespan or none.
        '''
        return self._timespan
