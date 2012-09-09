def timepoint_happens_when_timespan_starts(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens when `timespan` starts::

        >>> timespaninequalitytools.timepoint_happens_when_timespan_starts()
        TimepointInequality('timepoint == timespan.start')

    '''
    from experimental import timespaninequalitytools

    timepoint_inequality = timespaninequalitytools.TimepointInequality(
        'timepoint == timespan.start',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
