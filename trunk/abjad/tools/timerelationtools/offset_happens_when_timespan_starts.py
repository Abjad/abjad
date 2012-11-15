def offset_happens_when_timespan_starts(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make offset inequality indicating that `offset` happens when `timespan` starts::

        >>> timerelationtools.offset_happens_when_timespan_starts()
        OffsetTimespanTimeRelation('offset == timespan.start')

    '''
    from abjad.tools import timerelationtools

    offset_inequality = timerelationtools.OffsetTimespanTimeRelation(
        'offset == timespan.start',
        timespan=timespan, offset=offset)

    if offset_inequality.is_fully_loaded and not hold:
        return offset_inequality()
    else:
        return offset_inequality
