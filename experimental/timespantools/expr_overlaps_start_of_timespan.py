def expr_overlaps_start_of_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression overlaps start of timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_start_of_timespan()
        TimespanInequalityClass('expr.start < t.start < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityClass('expr.start < t.start < expr.stop')
