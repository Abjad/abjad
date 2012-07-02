def expr_starts_before_timespan_stops(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts before timespan stops::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_before_timespan_stops()
        TimespanInequalityTemplate('expr.start < t.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr.start < t.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
