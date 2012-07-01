def expr_starts_after_timespan_stops():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression starts after timespan stops::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_after_timespan_stops()
        TimespanInequalityTaxon('t.stop <= expr.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTaxon('t.stop <= expr.start')
