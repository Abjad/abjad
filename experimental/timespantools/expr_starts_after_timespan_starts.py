def expr_starts_after_timespan_starts(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_starts_after_timespan_starts()
        TimespanInequalityTemplate('expr_1.start < expr_2.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_1.start < expr_2.start')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
