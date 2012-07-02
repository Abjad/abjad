def expr_stops_before_timespan_starts():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_stops_before_timespan_starts()
        TimespanInequalityTemplate('expr.stop <= t.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTemplate('expr.stop <= t.start')
