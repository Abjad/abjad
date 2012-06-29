def expr_intersects_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression intersects timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_intersects_timespan()
        TimespanInequality('t.start <= expr.start < expr.stop or t.start < expr.stop <= expr.stop or t.start < expr.start < t.stop < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality(
        't.start <= expr.start < expr.stop or '
        't.start < expr.stop <= expr.stop or '
        't.start < expr.start < t.stop < expr.stop')
