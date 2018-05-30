def offset_happens_when_timespan_stops(timespan=None, offset=None, hold=False):
    """
    Makes time relation indicating that ``offset`` happens
    when ``timespan`` stops.

    ..  container:: example

        >>> relation = abjad.timespans.offset_happens_when_timespan_stops()
        >>> abjad.f(relation)
        abjad.timespans.OffsetTimespanTimeRelation(
            inequality=abjad.timespans.CompoundInequality(
                [
                    abjad.TimespanInequality('offset == timespan.stop'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    """
    from abjad import timespans

    inequality = timespans.CompoundInequality([
        'offset == timespan.stop',
        ])

    time_relation = timespans.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
