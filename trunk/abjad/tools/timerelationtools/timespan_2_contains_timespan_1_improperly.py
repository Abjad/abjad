def timespan_2_contains_timespan_1_improperly(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `timespan_2` contains `timespan_1` improperly::

        >>> timerelationtools.timespan_2_contains_timespan_1_improperly()
        TimespanTimespanTimeRelation('timespan_2.start <= timespan_1.start and timespan_1.stop <= timespan_2.stop')

    Return boolean or time relation.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_2.start <= timespan_1.start and timespan_1.stop <= timespan_2.stop',
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
