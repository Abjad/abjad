def timespan_2_starts_after_timespan_1_stops(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts after timespan stops::

        >>> from experimental import *

    ::

        >>> timetools.timespan_2_starts_after_timespan_1_stops()
        TimespanInequality('timespan_1.stop <= timespan_2.start')

    Return boolean or timespan inequality.
    '''
    from experimental import timetools

    timespan_inequality = timetools.TimespanInequality(
        'timespan_1.stop <= timespan_2.start',
        timespan_1=timespan_1, 
        timespan_2=timespan_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
