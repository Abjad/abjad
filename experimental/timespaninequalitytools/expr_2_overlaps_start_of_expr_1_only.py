def expr_2_overlaps_start_of_expr_1_only(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespaninequalitytools.expr_2_overlaps_start_of_expr_1_only()
        TimespanInequality('expr_2.start < expr_1.start < expr_2.start <= expr_1.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'expr_2.start < expr_1.start < expr_2.start <= expr_1.stop',
        expr_1=expr_1, 
        expr_2=expr_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
