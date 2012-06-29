def expr_overlaps_stop_of_timespan_only():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_stop_of_timespan_only()
        TimespanInequality('t.start <= expr.start < t.stop < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('t.start <= expr.start < t.stop < expr.stop')
