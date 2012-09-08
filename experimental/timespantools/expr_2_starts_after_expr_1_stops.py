def expr_2_starts_after_expr_1_stops(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts after timespan stops::

        >>> from experimental import *

    ::

        >>> timespantools.expr_2_starts_after_expr_1_stops()
        TimespanInequality('expr_1.stop <= expr_2.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    timespan_inequality = timespantools.TimespanInequality(
        'expr_1.stop <= expr_2.start',
        expr_1=expr_1, 
        expr_2=expr_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
