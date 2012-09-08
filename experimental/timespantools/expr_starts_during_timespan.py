def expr_starts_during_timespan(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality indicating that expression 2 starts during expression 1::

        >>> timespantools.expr_starts_during_timespan()
        TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop')

    Return timespan inequality or boolean.
    '''
    from experimental import timespantools

    timespan_inequality = timespantools.TimespanInequality(
        'expr_1.start <= expr_2.start < expr_1.stop',
        expr_1=expr_1,
        expr_2=expr_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
