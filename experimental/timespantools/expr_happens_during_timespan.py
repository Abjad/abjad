def expr_happens_during_timespan(timespan=None, expr=None):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality template indicating that expression happens during timespan::

        >>> timespantools.expr_happens_during_timespan()
        TimespanInequalityTemplate('t.start <= expr.start <= expr.stop <= t.stop')

    Make timespan inequality indicating that expression happens during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timespantools.expr_happens_during_timespan(timespan=selector)

    ::

        >>> z(timespan_inequality)
        timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start <= expr.stop <= t.stop'),
            timespantools.SingleSourceTimespan(
                selector=selectortools.SingleSegmentSelector(
                    identifier='red'
                    )
                )
            )

    Make timespan inequality indicating that offset ``7/16`` happens during segment ``'red'``::

        >>> timespan_inequality = timespantools.expr_happens_during_timespan(
        ...     selector, expr=durationtools.Offset(7, 16))

    ::

        >>> z(timespan_inequality)
        timespantools.TimespanInequality(
            timespantools.TimespanInequalityTemplate('t.start <= expr.start <= expr.stop <= t.stop'),
            timespantools.SingleSourceTimespan(
                selector=selectortools.SingleSegmentSelector(
                    identifier='red'
                    )
                ),
            expr=durationtools.Offset(7, 16)
            )

    Return timespan inequality template or timespan inequality.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start <= expr.start <= expr.stop <= t.stop')

    if timespan is None and expr is None:
        return template
    elif timespan is None and expr is not None:
        raise NotImplementedError
    elif timespan is not None:
        return timespantools.TimespanInequality(template, timespan, expr=expr)
    else:
        raise ValueError
