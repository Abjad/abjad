def timespan_2_contains_timespan_1_improperly(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make timespan inequality indicating that `timespan_2` contains `timespan_1` improperly::

        >>> timetools.timespan_2_contains_timespan_1_improperly()
        TimespanInequality('timespan_2.start <= timespan_1.start and timespan_1.stop <= timespan_2.stop')

    Return boolean or timespan inequality.
    '''
    from abjad.tools import timetools

    timespan_inequality = timetools.TimespanInequality(
        'timespan_2.start <= timespan_1.start and timespan_1.stop <= timespan_2.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
