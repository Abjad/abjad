def expr_starts_during_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression starts during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_during_timespan()
        TimespanInequalityTemplate('t.start <= expr.start < t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop')
