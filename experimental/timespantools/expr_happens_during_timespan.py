def expr_happens_during_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_happens_during_timespan()
        TimespanInequalityTemplate('t.start <= expr.start < expr.stop <= t.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start <= expr.start < expr.stop <= t.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
