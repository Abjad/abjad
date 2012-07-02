def expr_starts_after_timespan_stops(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts after timespan stops::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_after_timespan_stops()
        TimespanInequalityTemplate('t.stop <= expr.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.stop <= expr.start')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
