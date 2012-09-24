def timepoint_happens_after_timespan_stops(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens after `timespan` stops::

        >>> timetools.timepoint_happens_after_timespan_stops()
        TimepointInequality('timespan.stop < timepoint')

    '''
    from experimental import timetools

    timepoint_inequality = timetools.TimepointInequality(
        'timespan.stop < timepoint',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
