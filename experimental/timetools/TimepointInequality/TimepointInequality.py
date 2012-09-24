import fractions
from abjad.tools import durationtools
from experimental.timetools.Inequality import Inequality


class TimepointInequality(Inequality):
    r'''.. versionadded:: 1.0

    SymbolicTimepoint inequality.
    '''

    ### INITIALIZER ###

    def __init__(self, template, timespan=None, timepoint=None):
        Inequality.__init__(self, template)
        self._timespan = timespan
        self._timepoint = timepoint

    ### SPECIAL METHODS ###

    def __call__(self, timespan=None, timepoint=None):
        r'''Evaluate timepoint inequality.
        '''
        from experimental import timeobjecttools
        if timespan is None:
            timespan = self.timespan
        if timepoint is None:
            timepoint = self.timepoint
        if timespan is None or timepoint is None:
            raise ValueError('timepoint inequality is not fully loaded.')
        timespan = timeobjecttools.expr_to_timespan(timespan)
        timepoint = durationtools.Offset(timepoint)
        timespan_start = self._get_expr_start(timespan)
        timespan_stop = self._get_expr_stop(timespan)
        command = self.template
        command = command.replace('timespan.start', repr(timespan_start))
        command = command.replace('timespan.stop', repr(timespan_stop))
        command = command.replace('timepoint', repr(timepoint))
        result = eval(command, {'Offset': durationtools.Offset})
        return result

    def __eq__(self, expr):
        '''True when `expr` equals timepoint inequality. Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.template == expr.template:
                if self.timespan == expr.timespan:
                    if self.timepoint == expr.timepoint:
                        return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_fully_loaded(self):
        return self.timespan is not None and self.timepoint is not None

    @property
    def timepoint(self):
        return self._timepoint

    @property
    def timespan(self):
        return self._timespan
