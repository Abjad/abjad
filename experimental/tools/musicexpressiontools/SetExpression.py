# -*- encoding: utf-8 -*-
import abc
from abjad.tools import timerelationtools
from experimental.tools.musicexpressiontools.Expression import Expression


class SetExpression(Expression):
    r'''Set expression.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self, 
        attribute=None, 
        source_expression=None, 
        target_timespan=None,
        ):
        from experimental.tools import musicexpressiontools
        assert isinstance(attribute, str)
        assert isinstance(source_expression, musicexpressiontools.Expression)
        assert isinstance(target_timespan, 
            (timerelationtools.Timespan, musicexpressiontools.TimespanExpression,
            str, type(None)))
        self._attribute = attribute
        self._source_expression = source_expression
        self._target_timespan = target_timespan
        self._lexical_rank = None

    ### PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        r'''Set expression attribute.

        Returns string.
        '''
        return self._attribute

    @property
    def source_expression(self):
        r'''Set expression source expression.

        Returns expression.
        '''
        return self._source_expression

    @property
    def target_timespan(self):
        r'''Set expression target timespan.

        Returns timespan or timespan expression.
        '''
        return self._target_timespan

    @property
    def timespan(self):
        r'''Alias of set expression target timespan.

        Returns timespan or timespan expression.
        '''
        return self.target_timespan
