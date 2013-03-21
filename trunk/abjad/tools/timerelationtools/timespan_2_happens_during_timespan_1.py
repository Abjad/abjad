def timespan_2_happens_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that expression 2 happens during expression 1:

    ::

        >>> z(timerelationtools.timespan_2_happens_during_timespan_1())
        timerelationtools.TimespanTimespanTimeRelation(
            'timespan_1.start_offset <= timespan_2.start_offset <= timespan_2.stop_offset <= timespan_1.stop_offset',
            ['timespan_1.start_offset <= timespan_2.start_offset', 'timespan_2.start_offset <= timespan_2.stop_offset', 'timespan_2.stop_offset <= timespan_1.stop_offset']
            )

    Evaluate whether timespan ``[7/8, 8/8)`` happens during timespan ``[1/2, 3/2)``:

    ::

        >>> timespan_1 = timespantools.Timespan(Offset(1, 2), Offset(3, 2))
        >>> timespan_2 = timespantools.Timespan(Offset(7, 8), Offset(8, 8))
        >>> timerelationtools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=timespan_1, timespan_2=timespan_2)
        True

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.start_offset <= timespan_2.start_offset <= timespan_2.stop_offset <= timespan_1.stop_offset',
        [
            'timespan_1.start_offset <= timespan_2.start_offset',
            'timespan_2.start_offset <= timespan_2.stop_offset',
            'timespan_2.stop_offset <= timespan_1.stop_offset',
        ],
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
