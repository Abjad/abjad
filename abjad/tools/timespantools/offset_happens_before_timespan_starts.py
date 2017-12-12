def offset_happens_before_timespan_starts(
    timespan=None,
    offset=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `offset` happens before `timespan`
    starts.

    ..  container:: example

        Makes time relation indicating that `offset` happens before `timespan`
        starts:

        >>> relation = abjad.timespantools.offset_happens_before_timespan_starts()
        >>> abjad.f(relation)
        abjad.timespantools.OffsetTimespanTimeRelation(
            inequality=abjad.timespantools.CompoundInequality(
                [
                    abjad.TimespanInequality('offset < timespan.start'),
                    ],
                logical_operator='and',
                ),
            )

    ..  container:: example

        Makes time relation indicating that offset ``1/2`` happens before
        `timespan` starts:

        >>> offset = abjad.Offset(1, 2)

        >>> relation = \
        ...     abjad.timespantools.offset_happens_before_timespan_starts(
        ...     offset=offset)

        >>> abjad.f(relation)
        abjad.timespantools.OffsetTimespanTimeRelation(
            inequality=abjad.timespantools.CompoundInequality(
                [
                    abjad.TimespanInequality('offset < timespan.start'),
                    ],
                logical_operator='and',
                ),
            offset=abjad.Offset(1, 2),
            )

    ..  container:: example

        Makes time relation indicating that `offset` happens before timespan
        ``[2, 8)`` starts:

        >>> timespan = abjad.Timespan(2, 8)

        >>> relation = \
        ...     abjad.timespantools.offset_happens_before_timespan_starts(
        ...     timespan=timespan)

        >>> abjad.f(relation)
        abjad.timespantools.OffsetTimespanTimeRelation(
            inequality=abjad.timespantools.CompoundInequality(
                [
                    abjad.TimespanInequality('offset < timespan.start'),
                    ],
                logical_operator='and',
                ),
            timespan=abjad.Timespan(
                start_offset=abjad.Offset(2, 1),
                stop_offset=abjad.Offset(8, 1),
                ),
            )

    ..  container:: example

        Makes time relation indicating that offset ``1/2`` happens before
        timespan ``[2, 8)`` starts:

        >>> relation = abjad.timespantools.offset_happens_before_timespan_starts(
        ...     timespan=timespan,
        ...     offset=offset,
        ...     hold=True,
        ...     )

        >>> abjad.f(relation)
        abjad.timespantools.OffsetTimespanTimeRelation(
            inequality=abjad.timespantools.CompoundInequality(
                [
                    abjad.TimespanInequality('offset < timespan.start'),
                    ],
                logical_operator='and',
                ),
            timespan=abjad.Timespan(
                start_offset=abjad.Offset(2, 1),
                stop_offset=abjad.Offset(8, 1),
                ),
            offset=abjad.Offset(1, 2),
            )

    ..  container:: example

        Evaluates time relation indicating that offset ``1/2`` happens before
        timespan ``[2, 8)`` starts:

        >>> abjad.timespantools.offset_happens_before_timespan_starts(
        ...     timespan=timespan,
        ...     offset=offset,
        ...     hold=False,
        ...     )
        True

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'offset < timespan.start',
        ])

    time_relation = timespantools.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
