def expr_overlaps_all_of_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression overlaps all of timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_overlaps_all_of_timespan()
        TimespanInequalityTaxon('expr.start < t.start < t.stop < expr.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTaxon('expr.start < t.start < t.stop < expr.stop')
