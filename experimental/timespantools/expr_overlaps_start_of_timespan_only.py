def expr_overlaps_start_of_timespan_only():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_start_of_timespan_only()
        TimespanInequalityTaxon('expr.start < t.start < expr.start <= t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTaxon('expr.start < t.start < expr.start <= t.stop')
