def offset_happens_before_timespan_starts(timespan=None, offset=None, hold=False):
    r'''.. versionadded:: 2.11

    Make time relation indicating that `offset` happens before `timespan` starts::

        >>> timerelationtools.offset_happens_before_timespan_starts()
        OffsetTimespanTimeRelation('offset < timespan.start')

    Make time relation indicating that offset ``1/2`` happens before `timespan` starts::

        >>> offset = durationtools.Offset(1, 2)

    ::

        >>> time_relation = timerelationtools.offset_happens_before_timespan_starts(
        ...     offset=offset)

    ::

        >>> z(time_relation)
        timerelationtools.OffsetTimespanTimeRelation(
            'offset < timespan.start',
            offset=durationtools.Offset(1, 2)
            )

    Make time relation indicating that `offset` happens before timespan ``[2, 8)`` starts::

        >>> timespan = timerelationtools.expr_to_timespan((2, 8))

    ::

        >>> time_relation = timerelationtools.offset_happens_before_timespan_starts(
        ...     timespan=timespan)

    ::

        >>> z(time_relation)
        timerelationtools.OffsetTimespanTimeRelation(
            'offset < timespan.start',
            timespan=timerelationtools.LiteralTimespan(
                start_offset=durationtools.Offset(2, 1),
                stop_offset=durationtools.Offset(8, 1)
                )
            )

    Make time relation indicating that offset ``1/2`` happens before 
    timespan ``[2, 8)`` starts::

        >>> time_relation = timerelationtools.offset_happens_before_timespan_starts(
        ...     timespan=timespan, offset=offset, hold=True)

    ::

        >>> z(time_relation)
        timerelationtools.OffsetTimespanTimeRelation(
            'offset < timespan.start',
            timespan=timerelationtools.LiteralTimespan(
                start_offset=durationtools.Offset(2, 1),
                stop_offset=durationtools.Offset(8, 1)
                ),
            offset=durationtools.Offset(1, 2)
            )

    Evaluate time relation indicating that offset ``1/2`` happens before 
    timespan ``[2, 8)`` starts::

        >>> timerelationtools.offset_happens_before_timespan_starts(
        ...     timespan=timespan, offset=offset, hold=False)
        True

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        'offset < timespan.start',
        timespan=timespan, offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
