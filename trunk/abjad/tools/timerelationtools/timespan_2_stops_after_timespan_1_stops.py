def timespan_2_stops_after_timespan_1_stops(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation template indicating that `timespan_2` stops after `timespan_1` stops:

    ::

        >>> z(timerelationtools.timespan_2_stops_after_timespan_1_stops())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.stop_offset < timespan_2.stop_offset',
            ['timespan_1.stop_offset < timespan_2.stop_offset']
            )

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.stop_offset < timespan_2.stop_offset',
        [
            'timespan_1.stop_offset < timespan_2.stop_offset',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
