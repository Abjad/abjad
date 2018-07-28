from .TimeRelation import TimeRelation


class TimespanTimespanTimeRelation(TimeRelation):
    r"""
    Timespan vs. timespan time relation.

    Score for examples:

    ..  container:: example

        >>> string = r"\times 2/3 { c'4 d'4 e'4 } \times 2/3 { f'4 g'4 a'4 }"
        >>> staff_1 = abjad.Staff(string)
        >>> staff_2 = abjad.Staff("c'2. d'4")
        >>> score = abjad.Score([staff_1, staff_2])

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        f'4
                        g'4
                        a'4
                    }
                }
                \new Staff
                {
                    c'2.
                    d'4
                }
            >>

        >>> last_tuplet = staff_1[-1]
        >>> long_note = staff_2[0]

        >>> abjad.show(score) # doctest: +SKIP

    ..  container:: example

        >>> abjad.timespans.timespan_2_happens_during_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    ..  container:: example

        >>> abjad.timespans.timespan_2_intersects_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        True

    ..  container:: example

        >>> abjad.timespans.timespan_2_is_congruent_to_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    ..  container:: example

        >>> abjad.timespans.timespan_2_overlaps_all_of_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    ..  container:: example

        >>> abjad.timespans.timespan_2_overlaps_start_of_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        True

    ..  container:: example

        >>> abjad.timespans.timespan_2_overlaps_stop_of_timespan_1(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    ..  container:: example

        >>> abjad.timespans.timespan_2_starts_after_timespan_1_starts(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    ..  container:: example

        >>> abjad.timespans.timespan_2_starts_after_timespan_1_stops(
        ...     timespan_1=last_tuplet,
        ...     timespan_2=long_note,
        ...     )
        False

    Timespan / timespan time relations are immutable.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_timespan_1',
        '_timespan_2',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, inequality=None, timespan_1=None, timespan_2=None):
        TimeRelation.__init__(self, inequality=inequality)
        self._timespan_1 = timespan_1
        self._timespan_2 = timespan_2

    ### SPECIAL METHODS ###

    # TODO: hoist to TimeRelation
    def __call__(self, timespan_1=None, timespan_2=None):
        """
        Evaluate time relation.

        ..  container:: example

            Evaluate time relation without substitution:

            >>> timespan_1 = abjad.Timespan(5, 15)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

            >>> abjad.f(time_relation)
            abjad.timespans.TimespanTimespanTimeRelation(
                inequality=abjad.timespans.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan_1.start_offset <= timespan_2.start_offset'),
                        abjad.TimespanInequality('timespan_2.start_offset < timespan_1.stop_offset'),
                        ],
                    logical_operator='and',
                    ),
                timespan_1=abjad.Timespan(
                    start_offset=abjad.Offset(5, 1),
                    stop_offset=abjad.Offset(15, 1),
                    ),
                timespan_2=abjad.Timespan(
                    start_offset=abjad.Offset(10, 1),
                    stop_offset=abjad.Offset(20, 1),
                    ),
                )

            >>> time_relation()
            True

        ..  container:: example

            Substitute ``timespan_1`` during evaluation:

            >>> new_timespan_1 = abjad.Timespan(0, 10)

            >>> new_timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

            >>> time_relation(timespan_1=new_timespan_1)
            False

        ..  container:: example

            Substitute ``timespan_2`` during evaluation:

            >>> new_timespan_2 = abjad.Timespan(2, 12)

            >>> new_timespan_2
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(12, 1))

            >>> time_relation(timespan_2=new_timespan_2)
            False

        ..  container:: example

            Substitute both ``timespan_1`` and ``timespan_2`` during evaluation:

            >>> time_relation(
            ...     timespan_1=new_timespan_1,
            ...     timespan_2=new_timespan_2,
            ...     )
            True

        Raise value error if either ``timespan_1`` or ``timespan_2`` is none.

        Otherwise return boolean.
        """
        import abjad
        timespan_1 = timespan_1 or self.timespan_1
        timespan_2 = timespan_2 or self.timespan_2
        if timespan_1 is None or timespan_2 is None:
            message = 'time relation is not fully loaded: {!r}.'
            raise ValueError(message.format(self))
        if not isinstance(timespan_1, abjad.Timespan):
            timespan_1 = abjad.Timespan()._get_timespan(timespan_1)
        if not isinstance(timespan_2, abjad.Timespan):
            timespan_2 = abjad.Timespan()._get_timespan(timespan_2)
        truth_value = self.inequality.evaluate(
            timespan_1.start_offset, timespan_1.stop_offset,
            timespan_2.start_offset, timespan_2.stop_offset)
        return truth_value

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals time relation.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)
            >>> time_relation_1 = abjad.timespans.timespan_2_starts_during_timespan_1()
            >>> time_relation_2 = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)

            >>> time_relation_1 == time_relation_1
            True
            >>> time_relation_1 == time_relation_2
            False
            >>> time_relation_2 == time_relation_2
            True

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes time relation.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(TimespanTimespanTimeRelation, self).__hash__()

    ### PUBLIC METHODS ###

    def get_counttime_components(self, counttime_components):
        """
        Get ``counttime_components`` that satisfy ``time_relation``:

        ..  container:: example

            >>> notes = [abjad.Note(_ % 36, (1, 4)) for _ in range(200)]
            >>> voice = abjad.Voice(notes)
            >>> timespan_1 = abjad.Timespan(20, 22)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

            >>> result = time_relation.get_counttime_components(voice[:])

            >>> for counttime_component in result:
            ...     counttime_component
            Note("af'4")
            Note("a'4")
            Note("bf'4")
            Note("b'4")
            Note("c''4")
            Note("cs''4")
            Note("d''4")
            Note("ef''4")

            >>> abjad.inspect(result).timespan()
            Timespan(start_offset=Offset(20, 1), stop_offset=Offset(22, 1))

        ``counttime_components`` must belong to a single voice.

        ``counttime_components`` must be time-contiguous.

        The call shown here takes 78355 function calls under r9686.

        Returns selection.
        """
        import abjad
        # check input
        assert isinstance(counttime_components, (
            list, abjad.Selection)), repr(counttime_components)
        assert self.timespan_1 is not None
        # iterate counttime components
        result = []
        for counttime_component in counttime_components:
            if self(timespan_2=abjad.inspect(counttime_component).timespan()):
                result.append(counttime_component)
        # return result
        return abjad.select(result)

    def get_offset_indices(
        self,
        timespan_2_start_offsets,
        timespan_2_stop_offsets,
        ):
        """
        Get offset indices that satisfy time relation:

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> start_offsets = [
            ...     abjad.inspect(note).timespan().start_offset
            ...     for note in staff
            ...     ]
            >>> stop_offsets = [
            ...     abjad.inspect(note).timespan().stop_offset
            ...     for note in staff
            ...     ]

        ..  container:: example

            Notes equal to ``staff[0:2]`` start during timespan ``[0, 3/16)``:

            >>> timespan_1 = abjad.Timespan((0), (3, 16))
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     )
            >>> time_relation.get_offset_indices(start_offsets, stop_offsets)
            (0, 2)

        ..  container:: example

            Notes equal to ``staff[2:8]`` start after timespan ``[0, 3/16)``
            stops:

            >>> timespan_1 = abjad.Timespan((0), (3, 16))
            >>> time_relation =  abjad.timespans.timespan_2_starts_after_timespan_1_stops(
            ...     timespan_1=timespan_1,
            ...     )
            >>> time_relation.get_offset_indices(start_offsets, stop_offsets)
            (2, 8)

        Returns nonnegative integer pair.
        """
        result = self.inequality.get_offset_indices(
            self.timespan_1,
            timespan_2_start_offsets,
            timespan_2_stop_offsets,
            )
        if not result:
            return []
        elif len(result) == 1:
            timespan = result[0]
            start_index = int(timespan.start_offset)
            stop_index = int(timespan.stop_offset)
            return start_index, stop_index
        elif 0 < len(result):
            message = 'inequality evaluates to disjunct range: {!r}.'
            message = message.format(result)
            raise Exception(message)

    ### PUBLIC PROPERTIES ###

    @property
    def is_fully_loaded(self):
        """
        Is true when ``timespan_1`` and ``timespan_2`` are both not none.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

            >>> time_relation.is_fully_loaded
            True

        Returns true or false.
        """
        return self.timespan_1 is not None and self.timespan_2 is not None

    @property
    def is_fully_unloaded(self):
        """
        Is true when ``timespan_1`` and ``timespan_2`` are both none.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

            >>> time_relation.is_fully_unloaded
            False

        Returns true or false.
        """
        return self.timespan_1 is None and self.timespan_2 is None

    @property
    def timespan_1(self):
        """
        Time relation timespan ``1``:

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

            >>> time_relation.timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Returns timespan.
        """
        return self._timespan_1

    @property
    def timespan_2(self):
        """
        Time relation timespan ``2``:

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

            >>> time_relation.timespan_2
            Timespan(start_offset=Offset(5, 1), stop_offset=Offset(15, 1))

        Returns timespan.
        """
        return self._timespan_2
