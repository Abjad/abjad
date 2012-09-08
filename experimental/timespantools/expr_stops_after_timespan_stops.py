def expr_stops_after_timespan_stops(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression stops after timespan stops::

        >>> from experimental import *

    ::

        >>> timespantools.expr_stops_after_timespan_stops()
        TimespanInequalityTemplate('expr_1.stop < expr_2.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_1.stop < expr_2.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
