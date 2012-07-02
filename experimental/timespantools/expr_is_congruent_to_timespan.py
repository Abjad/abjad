def expr_is_congruent_to_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression is congruent to timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_is_congruent_to_timespan()
        TimespanInequalityTemplate('t.start == expr.start and t.stop == expr.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start == expr.start and t.stop == expr.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
