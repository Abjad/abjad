def timespan_2_overlaps_only_start_of_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation template indicating that expression happens during timespan:

    ::

        >>> z(timerelationtools.timespan_2_overlaps_only_start_of_timespan_1())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_2.start_offset < timespan_1.start_offset < timespan_2.stop_offset <= timespan_1.stop_offset',
            ['timespan_2.start_offset < timespan_1.start_offset', 'timespan_1.start_offset < timespan_2.stop_offset', 'timespan_2.stop_offset <= timespan_1.stop_offset']
            )

    Return boolean or time relation.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_2.start_offset < timespan_1.start_offset < timespan_2.stop_offset <= timespan_1.stop_offset',
        [
            'timespan_2.start_offset < timespan_1.start_offset',
            'timespan_1.start_offset < timespan_2.stop_offset',
            'timespan_2.stop_offset <= timespan_1.stop_offset',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
