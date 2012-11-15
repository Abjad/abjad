def timespan_2_stops_after_timespan_1_starts(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make timespan inequality template indicating that expression stops after timespan starts::

        >>> timerelationtools.timespan_2_stops_after_timespan_1_starts()
        TimespanTimespanTimeRelation('timespan_1.stop <= timespan_2.start')

    Return boolean or timespan inequality.
    '''
    from abjad.tools import timerelationtools

    timespan_inequality = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.stop <= timespan_2.start',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if timespan_inequality.is_fully_loaded and not hold:
        return timespan_inequality()
    else:
        return timespan_inequality
