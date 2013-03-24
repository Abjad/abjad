import abc
from abjad.tools import durationtools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.specificationtools.SetExpression import SetExpression


class TimespanScopedSingleContextSetExpression(SetExpression):
    '''Timespan-scoped single-context set expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, attribute=None, source_expression=None, target_timespan=None, target_context_name=None,
        fresh=None):
        assert isinstance(target_context_name, (str, type(None))), repr(target_context_name)
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        SetExpression.__init__(self, attribute=attribute, source_expression=source_expression, target_timespan=target_timespan)
        self._target_context_name = target_context_name
        self._fresh = fresh

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` is a timespan-scoped single-context set expression
        with same source_expression, target timespan and target context name.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_expression == expr.source_expression and \
                self.target_timespan == expr.target_timespan and \
                self.target_context_name == expr.target_context_name:
                return True
        return False

    def __lt__(self, expr):
        '''True when timespan-scoped single-context set expression target timespan
        is less than `expr` target_timespan.
        Otherwise false.

        Return boolean.
        '''
        if self.target_timespan.starts_before_timespan_starts(expr):
            return True
        elif self.target_timespan.starts_when_timespan_starts(expr):
            return self.target_timespan.stops_before_timespan_stops(expr)
        return False

    def __or__(self, set_expression):
        '''Logical OR of timespan-scoped single-context set expression and `set_expression`.

        Raise exception when timespan-scoped single-context set expression can not fuse with `set_expression`.

        Return timespan inventory.
        '''
        assert self._can_fuse(set_expression)
        stop_offset = self.target_timespan.stop_offset + set_expression.target_timespan.duration
        target_timespan = self.target_timespan.new(stop_offset=stop_offset)
        result = self.new(target_timespan=target_timespan)
        return timespantools.TimespanInventory([result])

    def __sub__(self, timespan):
        '''Subtract `timespan` from timespan-scoped single-context set expression.

        Operate in place and return timespan-scoped single-context set expression inventory.
        '''
        from experimental.tools import specificationtools
        timespans = self.target_timespan - timespan
        result = specificationtools.TimespanScopedSingleContextSetExpressionInventory()
        for timespan in timespans:
            region_expression = self.new(target_timespan=timespan)
            result.append(region_expression)
        return result

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _can_fuse(self, expr):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''True when set expression was generated in response
        to explicit user input. Otherwise false.

        Return boolean.
        '''
        return self._fresh

    # TODO: remove and use self.timespan.start_offset instead
    @property
    def start_offset(self):
        '''Set expression start offset.

        .. note:: remove and use ``self.timespan.start_offset`` instead.

        Return offset.
        '''
        return self.target_timespan.start_offset

    # TODO: remove and use self.timespan.stop_offset instead
    @property
    def stop_offset(self):
        '''Set expression stop offset.

        .. note:: remove and use ``self.timespan.stop_offset`` instead.

        Return offset.
        '''
        return self.target_timespan.stop_offset

    @property
    def target_context_name(self):
        '''Set expression context name.

        Return string.
        '''
        return self._target_context_name

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        '''Evaluate timespan-scoped single-context set expression.

        Return region expression.
        '''
        pass
