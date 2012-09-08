def expr_starts_before_timespan_stops(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts before timespan stops::

        >>> from experimental import *

    ::

        >>> timespantools.expr_starts_before_timespan_stops()
        TimespanInequalityTemplate('expr_2.start < expr_1.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_2.start < expr_1.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
