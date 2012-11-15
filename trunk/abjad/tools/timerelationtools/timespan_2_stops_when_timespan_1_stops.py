def timespan_2_stops_when_timespan_1_stops(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation template indicating that expression happens during timespan::

        >>> timerelationtools.timespan_2_stops_when_timespan_1_stops()
        TimespanTimespanTimeRelation('timespan_2.stop == timespan_1.stop')

    Return boolean or time relation.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_2.stop == timespan_1.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
