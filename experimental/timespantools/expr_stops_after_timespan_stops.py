def expr_stops_after_timespan_stops():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression stops after timespan stops::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_stops_after_timespan_stops()
        TimespanInequality('t.stop < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('t.stop < expr.stop')
