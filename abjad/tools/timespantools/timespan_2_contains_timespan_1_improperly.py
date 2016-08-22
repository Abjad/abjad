# -*- coding: utf-8 -*-


def timespan_2_contains_timespan_1_improperly(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` contains
    `timespan_1` improperly.

    ::

        >>> relation = timespantools.timespan_2_contains_timespan_1_improperly()
        >>> print(format(relation))
        timespantools.TimespanTimespanTimeRelation(
            inequality=timespantools.CompoundInequality(
                [
                    timespantools.Inequality('timespan_2.start_offset <= timespan_1.start_offset'),
                    timespantools.Inequality('timespan_1.stop_offset <= timespan_2.stop_offset'),
                    ],
                logical_operator='and',
                ),
            )

    ..  container:: example

        ::

            >>> staff = Staff(r"c'8. \p \< fs'16 a'4 af'8 \f \> g'8 ~ g'16 f' e' ef' \p")
            >>> timespan_1 = timespantools.Timespan(Offset(1, 4), Offset(3, 8))
            >>> show(staff) # doctest: +SKIP

        ::

            >>> offset_lists = staff[:]._get_offset_lists()
            >>> time_relation = timespantools.timespan_2_contains_timespan_1_improperly(timespan_1=timespan_1)
            >>> start_index, stop_index = time_relation.get_offset_indices(*offset_lists)
            >>> selected_notes = staff[start_index:stop_index]
            >>> selected_notes
            Selection([Note("a'4")])

        ::

            >>> label(selected_notes).color_leaves('red')
            >>> show(staff) # doctest: +SKIP

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan_2.start_offset <= timespan_1.start_offset',
        'timespan_1.stop_offset <= timespan_2.stop_offset',
        ])

    time_relation = timespantools.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
