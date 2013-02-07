import abc
from abjad.tools import timespantools
from experimental.tools.expressiontools.Expression import Expression


class SetExpression(Expression):
    '''Set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, source=None, target_timespan=None):
        from experimental.tools import expressiontools
        assert isinstance(source, expressiontools.Expression), repr(source)
        assert isinstance(target_timespan, (timespantools.Timespan, type(None))), repr(target_timespan)
        self._lexical_rank = None
        self._source = source
        self._target_timespan = target_timespan

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def target_timespan(self):
        return self._target_timespan
