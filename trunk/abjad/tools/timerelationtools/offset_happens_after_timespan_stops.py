def offset_happens_after_timespan_stops(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `offset` happens after `timespan` stops::

        >>> timerelationtools.offset_happens_after_timespan_stops()
        OffsetTimespanTimeRelation('timespan.stop < offset')

    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        'timespan.stop < offset',
        timespan=timespan, offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
