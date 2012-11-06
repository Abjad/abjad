def offset_happens_after_timespan_stops(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make offset inequality indicating that `offset` happens after `timespan` stops::

        >>> timerelationtools.offset_happens_after_timespan_stops()
        OffsetInequality('timespan.stop < offset')

    '''
    from abjad.tools import timerelationtools

    offset_inequality = timerelationtools.OffsetInequality(
        'timespan.stop < offset',
        timespan=timespan, offset=offset)

    if offset_inequality.is_fully_loaded and not hold:
        return offset_inequality()
    else:
        return offset_inequality
