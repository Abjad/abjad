def offset_happens_after_timespan_starts(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `offset` happens after `timespan` starts::

        >>> timerelationtools.offset_happens_after_timespan_starts()
        OffsetTimespanTimeRelation('timespan.start < offset')

    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        'timespan.start < offset',
        timespan=timespan, offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
