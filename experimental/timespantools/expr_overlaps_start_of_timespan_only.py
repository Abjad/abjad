def expr_overlaps_start_of_timespan_only(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_overlaps_start_of_timespan_only()
        TimespanInequalityTemplate('expr_2.start < expr_1.start < expr_2.start <= expr_1.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_2.start < expr_1.start < expr_2.start <= expr_1.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
