def offset_happens_when_timespan_starts(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make offset inequality indicating that `offset` happens when `timespan` starts::

        >>> timetools.offset_happens_when_timespan_starts()
        OffsetInequality('offset == timespan.start')

    '''
    from experimental import timetools

    offset_inequality = timetools.OffsetInequality(
        'offset == timespan.start',
        timespan=timespan, offset=offset)

    if offset_inequality.is_fully_loaded and not hold:
        return offset_inequality()
    else:
        return offset_inequality
