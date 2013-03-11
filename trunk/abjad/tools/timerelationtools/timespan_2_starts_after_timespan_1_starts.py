def timespan_2_starts_after_timespan_1_starts(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation template indicating that expression happens during timespan:

    ::

        >>> z(timerelationtools.timespan_2_starts_after_timespan_1_starts())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.start < timespan_2.start',
            ['timespan_1.start < timespan_2.start']
            )

    Return boolean or time relation.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.start < timespan_2.start',
        [
            'timespan_1.start < timespan_2.start',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
