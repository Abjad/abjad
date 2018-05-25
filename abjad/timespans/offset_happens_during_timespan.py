def offset_happens_during_timespan(timespan=None, offset=None, hold=False):
    """
    Makes time relation indicating that ``offset`` happens during ``timespan``.

    ..  container:: example

        >>> relation = abjad.timespans.offset_happens_during_timespan()
        >>> abjad.f(relation)
        abjad.timespans.OffsetTimespanTimeRelation(
            inequality=abjad.timespans.CompoundInequality(
                [
                    abjad.TimespanInequality('timespan.start <= offset'),
                    abjad.TimespanInequality('offset < timespan.stop'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    """
    from abjad import timespans

    inequality = timespans.CompoundInequality([
        'timespan.start <= offset',
        'offset < timespan.stop',
        ])

    time_relation = timespans.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
