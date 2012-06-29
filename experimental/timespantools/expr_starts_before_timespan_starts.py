def expr_starts_before_timespan_starts():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression starts before timespan starts::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_before_timespan_starts()
        TimespanInequality('expr.start < t.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('expr.start < t.start')
