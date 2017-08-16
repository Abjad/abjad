from abjad.tools import durationtools
from abjad.tools.timespantools.TimeRelation import TimeRelation


class OffsetTimespanTimeRelation(TimeRelation):
    r'''Offfset vs. timespan time relation.

    ..  container:: example

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )

        ::

            >>> f(time_relation)
            abjad.timespantools.OffsetTimespanTimeRelation(
                inequality=abjad.timespantools.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan.start <= offset'),
                        abjad.TimespanInequality('offset < timespan.stop'),
                        ],
                    logical_operator='and',
                    ),
                timespan=abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(10, 1),
                    ),
                offset=abjad.Offset(5, 1),
                )

    Offset / timespan time relations are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_offset',
        '_timespan',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, inequality=None, timespan=None, offset=None):
        TimeRelation.__init__(self, inequality=inequality)
        self._timespan = timespan
        self._offset = offset

    ### SPECIAL METHODS ###

    # TODO: hoist to TimeRelation
    def __call__(self, timespan=None, offset=None):
        r'''Evaluates time relation:

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> time_relation()
            True

        Raises value error is either `offset` or `timespan` is none.

        Otherwise returns boolean.
        '''
        from abjad.tools import timespantools
        timespan = timespan or self.timespan
        offset = offset or self.offset
        if timespan is None or offset is None:
            message = 'time relation is not fully loaded.'
            raise ValueError(message)
        if not isinstance(timespan, timespantools.Timespan):
            timespan = timespantools.Timespan()._get_timespan(timespan)
        offset = durationtools.Offset(offset)
        truth_value = self.inequality.evaluate_offset_inequality(
            timespan.start_offset, timespan.stop_offset, offset)
        return truth_value

    def __eq__(self, argument):
        r'''Is true when `argument` equals time relation. Otherwise false:

        ::

            >>> offset = abjad.Offset(5)
            >>> time_relation_1 = \
            ...     abjad.timespantools.offset_happens_during_timespan()
            >>> time_relation_2 = \
            ...     abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     )

        ::

            >>> time_relation_1 == time_relation_1
            True
            >>> time_relation_1 == time_relation_2
            False
            >>> time_relation_2 == time_relation_2
            True

        Returns true or false.
        '''
        return super(OffsetTimespanTimeRelation, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats time relation.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> f(time_relation)
            abjad.timespantools.OffsetTimespanTimeRelation(
                inequality=abjad.timespantools.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan.start <= offset'),
                        abjad.TimespanInequality('offset < timespan.stop'),
                        ],
                    logical_operator='and',
                    ),
                timespan=abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(10, 1),
                    ),
                offset=abjad.Offset(5, 1),
                )

        Returns string.
        '''
        superclass = super(OffsetTimespanTimeRelation, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes time relation.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(OffsetTimespanTimeRelation, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def is_fully_loaded(self):
        r'''Is true when `timespan` and `offset` are both not none.
        Otherwise false:

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> time_relation.is_fully_loaded
            True

        Returns true or false.
        '''
        return self.timespan is not None and self.offset is not None

    @property
    def is_fully_unloaded(self):
        r'''Is true when `timespan` and `offset` are both none.
        Otherwise false:

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> time_relation.is_fully_unloaded
            False

        Returns true or false.
        '''
        return self.timespan is None and self.offset is None

    @property
    def offset(self):
        r'''Time relation offset:

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> time_relation.offset
            Offset(5, 1)

        Returns offset or none.
        '''
        return self._offset

    @property
    def timespan(self):
        r'''Time relation timepsan:

        ::

            >>> offset = abjad.Offset(5)
            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation = abjad.timespantools.offset_happens_during_timespan(
            ...     offset=offset,
            ...     timespan=timespan,
            ...     hold=True,
            ...     )
            >>> time_relation.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Returns timespan or none.
        '''
        return self._timespan
