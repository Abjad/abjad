def offset_happens_after_timespan_starts(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make offset inequality indicating that `offset` happens after `timespan` starts::

        >>> timetools.offset_happens_after_timespan_starts()
        OffsetInequality('timespan.start < offset')

    '''
    from abjad.tools import timetools

    offset_inequality = timetools.OffsetInequality(
        'timespan.start < offset',
        timespan=timespan, offset=offset)

    if offset_inequality.is_fully_loaded and not hold:
        return offset_inequality()
    else:
        return offset_inequality
