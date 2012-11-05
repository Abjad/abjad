def offset_happens_after_timespan_stops(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens after `timespan` stops::

        >>> timetools.offset_happens_after_timespan_stops()
        OffsetInequality('timespan.stop < timepoint')

    '''
    from experimental import timetools

    timepoint_inequality = timetools.OffsetInequality(
        'timespan.stop < timepoint',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
