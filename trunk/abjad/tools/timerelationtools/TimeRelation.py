# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeRelation(AbjadObject):
    r'''A time relation.

    ::

        >>> timespan_1 = timespantools.Timespan(0, 10)
        >>> timespan_2 = timespantools.Timespan(5, 15)
        >>> time_relation = \
        ...     timerelationtools.timespan_2_starts_during_timespan_1(
        ...     timespan_1=timespan_1, 
        ...     timespan_2=timespan_2, 
        ...     hold=True,
        ...     )


    ::

        >>> print time_relation.storage_format
        timerelationtools.TimespanTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan_1.start_offset <= timespan_2.start_offset'),
                timerelationtools.SimpleInequality('timespan_2.start_offset < timespan_1.stop_offset')
                ],
                logical_operator='and'
                ),
            timespan_1=timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(10, 1)
                ),
            timespan_2=timespantools.Timespan(
                start_offset=durationtools.Offset(5, 1),
                stop_offset=durationtools.Offset(15, 1)
                )
            )

    Time relations are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality):
        from abjad.tools import timerelationtools
        assert isinstance(
            inequality, timerelationtools.CompoundInequality), repr(inequality)
        self._inequality = inequality

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Evaluate time relation:

        ::

            >>> time_relation()
            True

        Returns boolean.
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, expr):
        r'''True when `expr` is a equal-valued time relation.
        Otherwise false.

        Returns boolean.
        '''
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        r'''Time relation inequality.
        '''
        return self._inequality

    @abc.abstractproperty
    def is_fully_loaded(self):
        r'''True when both time relation terms are not none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_loaded
            True

        Returns boolean.
        '''
        pass

    @abc.abstractproperty
    def is_fully_unloaded(self):
        r'''True when both time relation terms are none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_unloaded
            False

        Returns boolean.
        '''
        pass

    @property
    def storage_format(self):
        r'''Time relation storage format:

        ::

            >>> print time_relation.storage_format
            timerelationtools.TimespanTimespanTimeRelation(
                timerelationtools.CompoundInequality([
                    timerelationtools.SimpleInequality('timespan_1.start_offset <= timespan_2.start_offset'),
                    timerelationtools.SimpleInequality('timespan_2.start_offset < timespan_1.stop_offset')
                    ],
                    logical_operator='and'
                    ),
                timespan_1=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespan_2=timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(15, 1)
                    )
                )

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        r'''Inialize new time relation with keyword arguments optionally changed:

        ::

            >>> time_relation = \
            ...     timerelationtools.timespan_2_stops_when_timespan_1_starts()
            >>> new_time_relation = \
            ...     time_relation.new(timespan_1=timespantools.Timespan(0, 5))

        ::

            >>> print time_relation.storage_format
            timerelationtools.TimespanTimespanTimeRelation(
                timerelationtools.CompoundInequality([
                    timerelationtools.SimpleInequality('timespan_2.stop_offset == timespan_1.start_offset')
                    ],
                    logical_operator='and'
                    )
                )

        ::

            >>> print new_time_relation.storage_format
            timerelationtools.TimespanTimespanTimeRelation(
                timerelationtools.CompoundInequality([
                    timerelationtools.SimpleInequality('timespan_2.stop_offset == timespan_1.start_offset')
                    ],
                    logical_operator='and'
                    ),
                timespan_1=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    )
                )

        Returns newly constructed time relation.
        '''
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            keyword_argument_dictionary[key] = value
        result = type(self)(
            *self._positional_argument_values, 
            **keyword_argument_dictionary
            )
        return result
