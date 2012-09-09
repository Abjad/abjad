import fractions
from abjad.tools import durationtools
from experimental.timespaninequalitytools.TimeObjectInequality import TimeObjectInequality


class TimepointInequality(TimeObjectInequality):
    r'''.. versionadded:: 1.0

    Timepoint inequality.
    '''

    ### INITIALIZER ###

    def __init__(self, template, timespan=None, timepoint=None):
        TimeObjectInequality.__init__(self, template)
        self._timespan = timespan
        self._timepoint = timepoint

    ### SPECIAL METHODS ###

    def __call__(self, timespan=None, timepoint=None):
        r'''Evaluate timepoint inequality.
        '''
        from experimental import timespantools
        if timespan is None:
            timespan = self.timespan
        if timepoint is None:
            timepoint = self.timepoint
        if timespan is None or timepoint is None:
            raise ValueError('timepoint inequality is not fully loaded.')
        timespan = timespantools.expr_to_timespan(timespan)
        timepoint = durationtools.Offset(timepoint)
        timespan_start = self._get_expr_start(timespan)
        timespan_stop = self._get_expr_stop(timespan)
        command = self.template
        command = command.replace('timespan.start', repr(timespan_start))
        command = command.replace('timespan.stop', repr(timespan_stop))
        command = command.replace('timepoint', repr(timepoint))
        result = eval(command, {'Offset': durationtools.Offset})
        return result
