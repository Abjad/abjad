def offset_happens_during_timespan(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make offset inequality indicating that `offset` happens during `timespan`::

        >>> timetools.offset_happens_during_timespan()
        OffsetInequality('timespan.start <= offset < timespan.stop')

    '''
    from abjad.tools import timetools

    offset_inequality = timetools.OffsetInequality(
        'timespan.start <= offset < timespan.stop',
        timespan=timespan, offset=offset)

    if offset_inequality.is_fully_loaded and not hold:
        return offset_inequality()
    else:
        return offset_inequality
