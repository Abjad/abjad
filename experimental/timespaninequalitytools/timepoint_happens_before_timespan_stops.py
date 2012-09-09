def timepoint_happens_before_timespan_stops(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens before `timespan` stops::

        >>> timespaninequalitytools.timepoint_happens_before_timespan_stops()
        TimepointInequality('timepoint < timespan.stop')

    '''
    from experimental import timespaninequalitytools

    timepoint_inequality = timespaninequalitytools.TimepointInequality(
        'timepoint < timespan.stop',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
