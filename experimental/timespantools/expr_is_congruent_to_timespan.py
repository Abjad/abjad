def expr_is_congruent_to_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression is congruent to timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_is_congruent_to_timespan()
        TimespanInequalityClass('t.start == expr.start and t.stop == expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityClass('t.start == expr.start and t.stop == expr.stop')
