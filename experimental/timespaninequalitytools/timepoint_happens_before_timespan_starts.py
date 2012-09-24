def timepoint_happens_before_timespan_starts(timespan=None, timepoint=None, hold=False):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Make timepoint inequality indicating that `timepoint` happens before `timespan` starts::

        >>> timespaninequalitytools.timepoint_happens_before_timespan_starts()
        TimepointInequality('timepoint < timespan.start')

    Make timepoint inequality indicating that timepoint ``1/2`` happens before `timespan` starts::

        >>> timepoint = durationtools.Offset(1, 2)

    ::

        >>> timepoint_inequality = timespaninequalitytools.timepoint_happens_before_timespan_starts(
        ...     timepoint=timepoint)

    ::

        >>> z(timepoint_inequality)
        timespaninequalitytools.TimepointInequality(
            'timepoint < timespan.start',
            timepoint=durationtools.Offset(1, 2)
            )

    Make timepoint inequality indicating that `timepoint` happens before timespan ``[2, 8)`` starts::

        >>> timespan = timespantools.expr_to_timespan((2, 8))

    ::

        >>> timepoint_inequality = timespaninequalitytools.timepoint_happens_before_timespan_starts(
        ...     timespan=timespan)

    ::

        >>> z(timepoint_inequality)
        timespaninequalitytools.TimepointInequality(
            'timepoint < timespan.start',
            timespan=durationtools.TimespanConstant(
                start_offset=durationtools.Offset(2, 1),
                stop_offset=durationtools.Offset(8, 1)
                )
            )

    Make timepoint inequality indicating that timepoint ``1/2`` happens before 
    timespan ``[2, 8)`` starts::

        >>> timepoint_inequality = timespaninequalitytools.timepoint_happens_before_timespan_starts(
        ...     timespan=timespan, timepoint=timepoint, hold=True)

    ::

        >>> z(timepoint_inequality)
        timespaninequalitytools.TimepointInequality(
            'timepoint < timespan.start',
            timespan=durationtools.TimespanConstant(
                start_offset=durationtools.Offset(2, 1),
                stop_offset=durationtools.Offset(8, 1)
                ),
            timepoint=durationtools.Offset(1, 2)
            )

    Evaluate timepoint inequality indicating that timepoint ``1/2`` happens before 
    timespan ``[2, 8)`` starts::

        >>> timespaninequalitytools.timepoint_happens_before_timespan_starts(
        ...     timespan=timespan, timepoint=timepoint, hold=False)
        True

    Return timepoint inequality or boolean.
    '''
    from experimental import timespaninequalitytools

    timepoint_inequality = timespaninequalitytools.TimepointInequality(
        'timepoint < timespan.start',
        timespan=timespan, timepoint=timepoint)

    if timepoint_inequality.is_fully_loaded and not hold:
        return timepoint_inequality()
    else:
        return timepoint_inequality
