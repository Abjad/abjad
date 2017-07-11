# -*- coding: utf-8 -*-


def timespan_2_starts_during_timespan_1(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` starts
    during `timespan_1`.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> relation = abjad.timespantools.timespan_2_starts_during_timespan_1()
            >>> f(relation)
            abjad.TimespanTimespanTimeRelation(
                inequality=abjad.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan_1.start_offset <= timespan_2.start_offset'),
                        abjad.TimespanInequality('timespan_2.start_offset < timespan_1.stop_offset'),
                        ],
                    logical_operator='and',
                    ),
                )

    ..  container:: example

        ::

            >>> staff_1 = abjad.Staff("c'4 d'4 e'4 f'4 g'2 c''2")
            >>> staff_2 = abjad.Staff("c'2 b'2 a'2 g'2")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> show(score) # doctest: +SKIP

        ::

            >>> start_offsets = [
            ...     abjad.inspect(note).get_timespan().start_offset
            ...     for note in staff_1
            ...     ]
            >>> stop_offsets = [
            ...     abjad.inspect(note).get_timespan().stop_offset
            ...     for note in staff_1
            ...     ]

        ::

            >>> timespan_1 = abjad.Timespan((1, 4), (5, 4))
            >>> time_relation = \
            ...     abjad.timespantools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)
            >>> start_index, stop_index = time_relation.get_offset_indices(
            ...     start_offsets, stop_offsets)

        ::

            >>> selected_notes = staff_1[start_index:stop_index]
            >>> selected_notes
            Selection([Note("d'4"), Note("e'4"), Note("f'4"), Note("g'2")])

        ::

            >>> abjad.label(selected_notes).color_leaves('red')

        ::

            >>> show(score) # doctest: +SKIP

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan_1.start_offset <= timespan_2.start_offset',
        'timespan_2.start_offset < timespan_1.stop_offset',
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
