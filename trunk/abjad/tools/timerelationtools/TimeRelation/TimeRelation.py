import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeRelation(AbjadObject):
    r'''.. versionadded:: 2.11

    Object-oriented time relation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, template):
        assert isinstance(template, str), repr(template)
        self._template = template

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
        pass

    @abc.abstractproperty
    def is_fully_unloaded(self):
        pass

    @property
    def template(self):
        '''Time relation template.

        Return string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    def set(self, **kwargs):
        '''Inialize new time relation with keyword arguments optionally changed::

            >>> time_relation = timerelationtools.timespan_2_stops_when_timespan_1_starts()
            >>> new_time_relation = time_relation.set(timespan_1=timespantools.Timespan(0, 5))

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
