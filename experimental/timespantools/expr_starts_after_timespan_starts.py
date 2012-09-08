def expr_starts_after_timespan_starts(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_starts_after_timespan_starts()
        TimespanInequality('expr_1.start < expr_2.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    timespan_inequality = timespantools.TimespanInequality(
        'expr_1.start < expr_2.start',
        expr_1=expr_1, 
        expr_2=expr_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
