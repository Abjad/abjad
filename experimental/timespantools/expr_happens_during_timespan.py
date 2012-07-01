def expr_happens_during_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_happens_during_timespan()
        TimespanInequalityTaxon('t.start <= expr.start < expr.stop <= t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTaxon('t.start <= expr.start < expr.stop <= t.stop')
