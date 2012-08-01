def expr_overlaps_stop_of_timespan_only(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_overlaps_stop_of_timespan_only()
        TimespanInequalityTemplate('t.start <= expr.start < t.stop < expr.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop < expr.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
