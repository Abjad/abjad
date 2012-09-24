def timespan_2_starts_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality indicating that expression 2 starts during expression 1::

        >>> timetools.timespan_2_starts_during_timespan_1()
        TimespanInequality('timespan_1.start <= timespan_2.start < timespan_1.stop')

    Return timespan inequality or boolean.
    '''
    from experimental import timetools

    timespan_inequality = timetools.TimespanInequality(
        'timespan_1.start <= timespan_2.start < timespan_1.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
