def offset_happens_when_timespan_starts(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens when `timespan` starts::

        >>> timetools.offset_happens_when_timespan_starts()
        OffsetInequality('timepoint == timespan.start')

    '''
    from experimental import timetools

    timepoint_inequality = timetools.OffsetInequality(
        'timepoint == timespan.start',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
