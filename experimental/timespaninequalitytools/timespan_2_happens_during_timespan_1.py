def timespan_2_happens_during_timespan_1(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality indicating that expression 2 happens during expression 1::

        >>> timespaninequalitytools.timespan_2_happens_during_timespan_1()
        TimespanInequality('expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop')

    Make timespan inequality indicating that expression 2 happens during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timespaninequalitytools.timespan_2_happens_during_timespan_1(expr_1=selector)

    ::

        >>> z(timespan_inequality)
        timespaninequalitytools.TimespanInequality(
            'expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop',
            expr_1=selectortools.SingleSegmentSelector(
                identifier='red'
                )
            )

    Make timespan inequality indicating that offset ``7/16`` happens during segment ``'red'``::

        >>> timespan_inequality = timespaninequalitytools.timespan_2_happens_during_timespan_1(
        ...     expr_1=selector, expr_2=durationtools.Offset(7, 16), hold=True)

    ::

        >>> z(timespan_inequality)
        timespaninequalitytools.TimespanInequality(
            'expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop',
            expr_1=selectortools.SingleSegmentSelector(
                identifier='red'
                ),
            expr_2=durationtools.Offset(7, 16)
            )

    Evaluate whether timespan ``[7/8, 8/8)`` happens during timespan ``[1/2, 3/2)``::

        >>> timespaninequalitytools.timespan_2_happens_during_timespan_1(
        ...     expr_1=((1, 2), (3, 2)), expr_2=((7, 8), (8, 8)))
        True

    Evaluate whether offset ``7/8`` happens during timespan ``[1/2, 3/2)``::

        >>> timespaninequalitytools.timespan_2_happens_during_timespan_1(
        ...     expr_1=((1, 2), (3, 2)), expr_2=durationtools.Offset(7, 8))
        True

    Return timespan inequality or boolean.
    '''
    from experimental import timespaninequalitytools

    timespan_inequality = timespaninequalitytools.TimespanInequality(
        'expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop',
        expr_1=expr_1, 
        expr_2=expr_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
