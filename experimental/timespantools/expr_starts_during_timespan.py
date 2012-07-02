def expr_starts_during_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_during_timespan()
        TimespanInequalityTemplate('t.start <= expr.start < t.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
