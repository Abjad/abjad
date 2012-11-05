def offset_happens_after_timespan_starts(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens after `timespan` starts::

        >>> timetools.offset_happens_after_timespan_starts()
        TimepointInequality('timespan.start < timepoint')

    '''
    from experimental import timetools

    timepoint_inequality = timetools.TimepointInequality(
        'timespan.start < timepoint',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
