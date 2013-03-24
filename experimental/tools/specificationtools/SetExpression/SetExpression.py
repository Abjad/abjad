import abc
from abjad.tools import timespantools
from experimental.tools.specificationtools.Expression import Expression


class SetExpression(Expression):
    '''Set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, source_expression=None, target_timespan=None):
        from experimental.tools import specificationtools
        assert isinstance(attribute, str), repr(attribute)
        assert isinstance(source_expression, specificationtools.Expression), repr(source_expression)
        assert isinstance(target_timespan, (timespantools.Timespan, specificationtools.TimespanExpression,
            str, type(None))), repr(target_timespan)
        self._attribute = attribute
        self._source_expression = source_expression
        self._target_timespan = target_timespan
        self._lexical_rank = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Set expression attribute.

        Return string.
        '''
        return self._attribute

    @property
    def source_expression(self):
        '''Set expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def target_timespan(self):
        '''Set expression target timespan.

        Return timespan or timespan expression.
        '''
        return self._target_timespan

    @property
    def timespan(self):
        '''Alias of set expression target timespan.

        Return timespan or timespan expression.
        '''
        return self.target_timespan
