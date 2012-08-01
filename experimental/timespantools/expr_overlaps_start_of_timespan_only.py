def expr_overlaps_start_of_timespan_only(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_overlaps_start_of_timespan_only()
        TimespanInequalityTemplate('expr.start < t.start < expr.start <= t.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr.start < t.start < expr.start <= t.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
