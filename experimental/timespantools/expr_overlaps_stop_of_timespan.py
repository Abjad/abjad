def expr_overlaps_stop_of_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression overlaps stop of timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_stop_of_timespan()
        TimespanInequalityClass('expr.start < t.stop < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityClass('expr.start < t.stop < expr.stop')
