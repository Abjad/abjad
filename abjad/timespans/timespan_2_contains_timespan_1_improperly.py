def timespan_2_contains_timespan_1_improperly(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r"""
    Makes time relation indicating that ``timespan_2`` contains
    ``timespan_1`` improperly.

    ..  container:: example

        >>> relation = abjad.timespans.timespan_2_contains_timespan_1_improperly()
        >>> abjad.f(relation)
        abjad.timespans.TimespanTimespanTimeRelation(
            inequality=abjad.timespans.CompoundInequality(
                [
                    abjad.TimespanInequality('timespan_2.start_offset <= timespan_1.start_offset'),
                    abjad.TimespanInequality('timespan_1.stop_offset <= timespan_2.stop_offset'),
                    ],
                logical_operator='and',
                ),
            )

    ..  container:: example

        >>> staff = abjad.Staff(
        ...     r"c'8. \p \< fs'16 a'4 af'8 \f \> g'8 ~ g'16 f' e' ef' \p",
        ...     )
        >>> timespan_1 = abjad.Timespan((1, 4), (3, 8))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> offset_lists = staff[:]._get_offset_lists()
        >>> time_relation = abjad.timespans.timespan_2_contains_timespan_1_improperly(timespan_1=timespan_1)
        >>> start_index, stop_index = time_relation.get_offset_indices(*offset_lists)
        >>> selected_notes = staff[start_index:stop_index]
        >>> selected_notes
        Selection([Note("a'4")])

        >>> abjad.label(selected_notes).color_leaves('red')
        >>> abjad.show(staff) # doctest: +SKIP

    Returns time relation or boolean.
    """
    from abjad import timespans

    inequality = timespans.CompoundInequality([
        'timespan_2.start_offset <= timespan_1.start_offset',
        'timespan_1.stop_offset <= timespan_2.stop_offset',
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
