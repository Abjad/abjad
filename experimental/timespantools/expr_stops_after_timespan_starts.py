def expr_stops_after_timespan_starts(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression stops after timespan starts::

        >>> from experimental import *

    ::

        >>> timespantools.expr_stops_after_timespan_starts()
        TimespanInequalityTemplate('t.stop <= expr.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.stop <= expr.start')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
