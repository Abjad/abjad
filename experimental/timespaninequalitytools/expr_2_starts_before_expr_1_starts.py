def expr_2_starts_before_expr_1_starts(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts before timespan starts::

        >>> from experimental import *

    ::

        >>> timespaninequalitytools.expr_2_starts_before_expr_1_starts()
        TimespanInequality('expr_2.start < expr_1.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'expr_2.start < expr_1.start',
        expr_1=expr_1, 
        expr_2=expr_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
