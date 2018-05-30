def timespan_2_stops_before_timespan_1_stops(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    """
    Makes time relation indicating that ``timespan_2``
    happens during ``timespan_1``.

    ..  container:: example

        >>> time_relation = abjad.timespans.timespan_2_stops_before_timespan_1_stops()
        >>> abjad.f(time_relation)
        abjad.timespans.TimespanTimespanTimeRelation(
            inequality=abjad.timespans.CompoundInequality(
                [
                    abjad.TimespanInequality('timespan_2.stop_offset < timespan_1.stop_offset'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    """
    from abjad import timespans

    time_relation = timespans.TimespanTimespanTimeRelation(
        timespans.CompoundInequality([
            'timespan_2.stop_offset < timespan_1.stop_offset',
            ]),
        timespan_1=timespan_1,
        timespan_2=timespan_2)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
