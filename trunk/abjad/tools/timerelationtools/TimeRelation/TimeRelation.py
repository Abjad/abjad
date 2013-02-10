import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeRelation(AbjadObject):
    r'''.. versionadded:: 2.11

    Time relation:

    ::

        >>> timespan_1 = timespantools.Timespan(0, 10)
        >>> timespan_2 = timespantools.Timespan(5, 15)
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
        ...     timespan_1=timespan_1, timespan_2=timespan_2, hold=True)


    ::

        >>> z(time_relation)
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.start <= timespan_2.start < timespan_1.stop',
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

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, template):
        assert isinstance(template, str), repr(template)
        self._template = template

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        '''Evaluate time relation:

        ::

            >>> time_relation()
            True
    
        Return boolean.
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, expr):
        '''True when `expr` is a time relation with
        template and both terms equal to time relation.
        Otherwise false.
    
        Return boolean.
        '''
        pass

    ### PRIVATE METHODS ###

    def _get_expr_offsets(self, expr, score_specification=None, context_name=None):
        if hasattr(expr, 'offsets'):
            return expr.offsets
        elif hasattr(expr, 'get_offsets'):
            return expr.get_offsets(score_specification, context_name)
        else:
            raise ValueError('{!r} has neither offsets property nor get_offsets() method.'.format(expr))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_fully_loaded(self):
        '''True when both time relation terms are not none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_loaded
            True
    
        Return boolean.
        '''
        pass

    @abc.abstractproperty
    def is_fully_unloaded(self):
        '''True when both time relation terms are none.
        Otherwise false:

        ::

            >>> time_relation.is_fully_unloaded
            False
    
        Return boolean.
        '''
        pass

    @property
    def storage_format(self):
        '''Time relation storage format:

        ::

            >>> z(time_relation)
            timerelationtools.TimespanTimespanTimeRelation(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespan_2=timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(15, 1)
                    )
                )

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    @property
    def template(self):
        '''Time relation template:
    
        ::

            >>> time_relation.template
            'timespan_1.start <= timespan_2.start < timespan_1.stop'

        Return string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        '''Inialize new time relation with keyword arguments optionally changed:

        ::

            >>> time_relation = timerelationtools.timespan_2_stops_when_timespan_1_starts()
            >>> new_time_relation = time_relation.new(timespan_1=timespantools.Timespan(0, 5))

        ::

            >>> z(time_relation)
            timerelationtools.TimespanTimespanTimeRelation(
                'timespan_2.stop == timespan_1.start'
                )

        ::

            >>> z(new_time_relation)
            timerelationtools.TimespanTimespanTimeRelation(
                'timespan_2.stop == timespan_1.start',
                timespan_1=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    )
                )

        Return newly constructed time relation.
        '''
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            keyword_argument_dictionary[key] = value
        result = type(self)(*self._positional_argument_values, **keyword_argument_dictionary)
        return result
