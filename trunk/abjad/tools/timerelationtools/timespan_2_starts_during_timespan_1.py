def timespan_2_starts_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that expression 2 starts during expression 1:

    ::

        >>> z(timerelationtools.timespan_2_starts_during_timespan_1())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.start <= timespan_2.start < timespan_1.stop',
            ['timespan_1.start <= timespan_2.start', 'timespan_2.start < timespan_1.stop']
            )

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.start <= timespan_2.start < timespan_1.stop',
        [
            'timespan_1.start <= timespan_2.start',
            'timespan_2.start < timespan_1.stop',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)


    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
