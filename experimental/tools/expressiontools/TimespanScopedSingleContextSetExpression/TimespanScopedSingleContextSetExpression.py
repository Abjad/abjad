import abc
from abjad.tools import durationtools
from abjad.tools import timerelationtools 
from abjad.tools import timespantools 
from experimental.tools.expressiontools.SetExpression import SetExpression


# TODO: maybe doesn't need to inherit (indirectly) from AnchoredExpression; no longer has anchor
class TimespanScopedSingleContextSetExpression(SetExpression):
    '''Timespan-scoped single-context set expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    def __init__(self, source=None, timespan=None, context_name=None, fresh=None):
        from experimental.tools import expressiontools
        assert isinstance(source, (expressiontools.Expression)), repr(sourcd)
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        assert isinstance(fresh, (bool, type(None))), repr(fresh)
        SetExpression.__init__(self, source=source)
        self._timespan = timespan
        self._context_name = context_name
        self._fresh = fresh

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.source == expr.source and \
                self.context_name == expr.context_name and \
                self.timespan == expr.timespan:
                return True
        return False

    def __lt__(self, expr):
        if self.timespan.starts_before_timespan_starts(expr):
            return True
        elif self.timespan.starts_when_timespan_starts(expr):
            return self.timespan.stops_before_timespan_stops(expr)
        return False

    def __or__(self, command):
        '''Logical OR of region command and `command`.

        Return newly constructed region command.

        Raise exception when region command can not fuse with `command`.
        '''
        assert self._can_fuse(command)
        stop_offset = self.timespan.stop_offset + command.timespan.duration
        timespan = self.timespan.new(stop_offset=stop_offset) 
        result = self.new(timespan=timespan)
        return timespantools.TimespanInventory([result])

    def __sub__(self, timespan):
        '''Subtract `timespan` from region command.

        Operate in place and return region command inventory.
        '''
        from experimental.tools import expressiontools
        timespans = self.timespan - timespan
        result = expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for timespan in timespans:
            region_expression = self.new(timespan=timespan)
            result.append(region_expression)
        return result

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _can_fuse(self, expr):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def attribute(self):
        '''Set expression attribute.

        Return string.
        '''
        pass

    @property
    def context_name(self):
        '''Set expression context name.
    
        Return string.
        '''
        return self._context_name

    @property
    def fresh(self):
        '''True when region command was generated in response 
        to an explicit user command. Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def start_offset(self):
        '''Set expression start offset.

        Return offset.
        '''
        return self.timespan.start_offset

    @property
    def stop_offset(self):
        '''Set expression stop offset.

        Return offset.
        '''
        return self.timespan.stop_offset

    @property
    def timespan(self):
        '''Set expression timespan.

        Return timespan.
        '''
        return self._timespan

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        '''Evaluate timespan-scoped single-context set expression.
        
        Return region expression.
        '''
        pass
