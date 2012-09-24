def timespan_2_happens_during_timespan_1(timespan_1=None, timespan_2=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timespan inequality indicating that expression 2 happens during expression 1::

        >>> timetools.timespan_2_happens_during_timespan_1()
        TimespanInequality('timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop')

    Make timespan inequality indicating that expression 2 happens during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timetools.timespan_2_happens_during_timespan_1(timespan_1=selector)

    ::

        >>> z(timespan_inequality)
        timetools.TimespanInequality(
            'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',
            timespan_1=selectortools.SingleSegmentSelector(
                identifier='red'
                )
            )

    Make timespan inequality indicating that offset ``7/16`` happens during segment ``'red'``::

        >>> timespan_inequality = timetools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=selector, timespan_2=durationtools.Offset(7, 16), hold=True)

    ::

        >>> z(timespan_inequality)
        timetools.TimespanInequality(
            'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',
            timespan_1=selectortools.SingleSegmentSelector(
                identifier='red'
                ),
            timespan_2=durationtools.Offset(7, 16)
            )

    Evaluate whether timespan ``[7/8, 8/8)`` happens during timespan ``[1/2, 3/2)``::

        >>> timetools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=((1, 2), (3, 2)), timespan_2=((7, 8), (8, 8)))
        True

    Evaluate whether offset ``7/8`` happens during timespan ``[1/2, 3/2)``::

        >>> timetools.timespan_2_happens_during_timespan_1(
        ...     timespan_1=((1, 2), (3, 2)), timespan_2=durationtools.Offset(7, 8))
        True

    Return timespan inequality or boolean.
    '''
    from experimental import timetools

    timespan_inequality = timetools.TimespanInequality(
        'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',
        timespan_1=timespan_1, 
        timespan_2=timespan_2)
    
    if timespan_inequality.is_fully_loaded and not hold: 
        return timespan_inequality()
    else:
        return timespan_inequality
