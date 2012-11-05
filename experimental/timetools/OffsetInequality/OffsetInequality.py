import fractions
from abjad.tools import durationtools
from experimental.timetools.Inequality import Inequality


class OffsetInequality(Inequality):
    r'''.. versionadded:: 1.0

    SymbolicOffset inequality.
    '''

    ### INITIALIZER ###

    def __init__(self, template, timespan=None, offset=None):
        Inequality.__init__(self, template)
        self._timespan = timespan
        self._offset = offset

    ### SPECIAL METHODS ###

    def __call__(self, timespan=None, offset=None):
        r'''Evaluate offset inequality.
        '''
        from experimental import timetools
        if timespan is None:
            timespan = self.timespan
        if offset is None:
            offset = self.offset
        if timespan is None or offset is None:
            raise ValueError('offset inequality is not fully loaded.')
        timespan = timetools.expr_to_timespan(timespan)
        offset = durationtools.Offset(offset)
        timespan_start = self._get_expr_start(timespan)
        timespan_stop = self._get_expr_stop(timespan)
        command = self.template
        command = command.replace('timespan.start', repr(timespan_start))
        command = command.replace('timespan.stop', repr(timespan_stop))
        command = command.replace('offset', repr(offset))
        result = eval(command, {'Offset': durationtools.Offset})
        return result

    def __eq__(self, expr):
        '''True when `expr` equals offset inequality. Otherwise false.

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
        return self.timespan is not None and self.offset is not None

    @property
    def offset(self):
        return self._offset

    @property
    def timespan(self):
        return self._timespan
