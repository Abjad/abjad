def expr_starts_when_timespan_starts():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression starts when timespan starts::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_when_timespan_starts()
        TimespanInequalityTaxon('t.start == expr.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTaxon('t.start == expr.start')
