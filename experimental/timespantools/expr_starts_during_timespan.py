def expr_starts_during_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression starts during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_during_timespan()
        TimespanInequality('t.start <= expr.start < t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('t.start <= expr.start < t.stop')
