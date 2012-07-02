def expr_overlaps_all_of_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression overlaps all of timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_all_of_timespan()
        TimespanInequalityTemplate('expr.start < t.start < t.stop < expr.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr.start < t.start < t.stop < expr.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
