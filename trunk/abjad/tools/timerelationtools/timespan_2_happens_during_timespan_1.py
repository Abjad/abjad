def timespan_2_happens_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 2.11

    Make timespan inequality indicating that expression 2 happens during expression 1::

        >>> timerelationtools.timespan_2_happens_during_timespan_1()
        TimespanTimespanTimeRelation('timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop')

    Evaluate whether timespan ``[7/8, 8/8)`` happens during timespan ``[1/2, 3/2)``::

        >>> timerelationtools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=((1, 2), (3, 2)), timespan_2=((7, 8), (8, 8)))
        True

    Evaluate whether offset ``7/8`` happens during timespan ``[1/2, 3/2)``::

        >>> timerelationtools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=((1, 2), (3, 2)), timespan_2=durationtools.Offset(7, 8))
        True

    Return timespan inequality or boolean.
    '''
    from abjad.tools import timerelationtools

    timespan_inequality = timerelationtools.TimespanTimespanTimeRelation(
        'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',
        timespan_1=timespan_1, 
        timespan_2=timespan_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
