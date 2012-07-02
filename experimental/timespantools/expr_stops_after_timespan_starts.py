def expr_stops_after_timespan_starts():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression stops after timespan starts::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_stops_after_timespan_starts()
        TimespanInequalityTemplate('t.stop <= expr.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTemplate('t.stop <= expr.start')
