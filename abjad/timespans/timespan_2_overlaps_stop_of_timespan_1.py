def timespan_2_overlaps_stop_of_timespan_1(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    """
    Make time relation indicating that ``timespan_2`` overlaps stop of
    ``timespan_1``.

    ..  container:: example

        >>> relation = abjad.timespans.timespan_2_overlaps_stop_of_timespan_1()
        >>> abjad.f(relation)
        abjad.timespans.TimespanTimespanTimeRelation(
            inequality=abjad.timespans.CompoundInequality(
                [
                    abjad.TimespanInequality('timespan_2.start_offset < timespan_1.stop_offset'),
                    abjad.TimespanInequality('timespan_1.stop_offset < timespan_2.stop_offset'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    """
    from abjad import timespans

    inequality = timespans.CompoundInequality([
        'timespan_2.start_offset < timespan_1.stop_offset',
        'timespan_1.stop_offset < timespan_2.stop_offset',
        ])

    time_relation = timespans.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
