def timespan_2_stops_before_timespan_1_stops(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespaninequalitytools.timespan_2_stops_before_timespan_1_stops()
        TimespanInequality('expr_2.stop < expr_1.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'expr_2.stop < expr_1.stop',
        expr_1=expr_1,
        expr_2=expr_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
