# -*- coding: utf-8 -*-
from abjad.tools.timespantools.TimeRelation import TimeRelation


class TimespanTimespanTimeRelation(TimeRelation):
    r'''A timespan vs. timespan time relation.

    Score for examples:

    ::

        >>> staff_1 = Staff(
        ...     r"\times 2/3 { c'4 d'4 e'4 } \times 2/3 { f'4 g'4 a'4 }")
        >>> staff_2 = Staff("c'2. d'4")
        >>> score = Score([staff_1, staff_2])

    ..  doctest::

        >>> print(format(score))
        \new Score <<
            \new Staff {
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
            \new Staff {
                c'2.
                d'4
            }
        >>

    ::

        >>> last_tuplet = staff_1[-1]
        >>> long_note = staff_2[0]

    ::

        >>> show(score) # doctest: +SKIP

    ..  container:: example

       **Example 1:**

        ::

            >>> timespantools.timespan_2_happens_during_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    ..  container:: example

       **Example 2:**

        ::

            >>> timespantools.timespan_2_intersects_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            True

    ..  container:: example

       **Example 3:**

        ::

            >>> timespantools.timespan_2_is_congruent_to_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    ..  container:: example

       **Example 4:**

        ::

            >>> timespantools.timespan_2_overlaps_all_of_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    ..  container:: example

       **Example 5:**

        ::

            >>> timespantools.timespan_2_overlaps_start_of_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            True

    ..  container:: example

       **Example 6:**

        ::

            >>> timespantools.timespan_2_overlaps_stop_of_timespan_1(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    ..  container:: example

       **Example 7:**

        ::

            >>> timespantools.timespan_2_starts_after_timespan_1_starts(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    ..  container:: example

       **Example 8:**

        ::

            >>> timespantools.timespan_2_starts_after_timespan_1_stops(
            ...     timespan_1=last_tuplet,
            ...     timespan_2=long_note,
            ...     )
            False

    Timespan / timespan time relations are immutable.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_timespan_1',
        '_timespan_2',
        )

    ### INITIALIZER ###

    def __init__(self, inequality=None, timespan_1=None, timespan_2=None):
        TimeRelation.__init__(self, inequality=inequality)
        self._timespan_1 = timespan_1
        self._timespan_2 = timespan_2

    ### SPECIAL METHODS ###

    # TODO: hoist to TimeRelation
    def __call__(self, timespan_1=None, timespan_2=None):
        r'''Evaluate time relation.

        ..  container:: example

            **Example 1.** Evaluate time relation without substitution:

            ::

                >>> timespan_1 = timespantools.Timespan(5, 15)
                >>> timespan_2 = timespantools.Timespan(10, 20)

            ::

                >>> time_relation = timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan_1,
                ...     timespan_2=timespan_2,
                ...     hold=True,
                ...     )

            ::

                >>> print(format(time_relation))
                timespantools.TimespanTimespanTimeRelation(
                    inequality=timespantools.CompoundInequality(
                        [
                            timespantools.Inequality('timespan_1.start_offset <= timespan_2.start_offset'),
                            timespantools.Inequality('timespan_2.start_offset < timespan_1.stop_offset'),
                            ],
                        logical_operator='and',
                        ),
                    timespan_1=timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(15, 1),
                        ),
                    timespan_2=timespantools.Timespan(
                        start_offset=durationtools.Offset(10, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    )

            ::

                >>> time_relation()
                True

        ..  container:: example

            **Example 2.** Substitute `timespan_1` during evaluation:

            ::

                >>> new_timespan_1 = timespantools.Timespan(0, 10)

            ::

                >>> new_timespan_1
                Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

            ::

                >>> time_relation(timespan_1=new_timespan_1)
                False

        ..  container:: example

            **Example 3.** Substitute `timespan_2` during evaluation:

            ::

                >>> new_timespan_2 = timespantools.Timespan(2, 12)

            ::

                >>> new_timespan_2
                Timespan(start_offset=Offset(2, 1), stop_offset=Offset(12, 1))

            ::

                >>> time_relation(timespan_2=new_timespan_2)
                False

        ..  container:: example

            **Example 4.** Substitute both `timespan_1` and `timespan_2`
            during evaluation:

            ::

                >>> time_relation(
                ...     timespan_1=new_timespan_1,
                ...     timespan_2=new_timespan_2,
                ...     )
                True

        Raise value error if either `timespan_1` or `timespan_2` is none.

        Otherwise return boolean.
        '''
        from abjad.tools import timespantools
        timespan_1 = timespan_1 or self.timespan_1
        timespan_2 = timespan_2 or self.timespan_2
        if timespan_1 is None or timespan_2 is None:
            message = 'time relation is not fully loaded: {!r}.'
            raise ValueError(message.format(self))
        if not isinstance(timespan_1, timespantools.Timespan):
            timespan_1 = timespantools.Timespan()._get_timespan(timespan_1)
        if not isinstance(timespan_2, timespantools.Timespan):
            timespan_2 = timespantools.Timespan()._get_timespan(timespan_2)
        truth_value = self.inequality.evaluate(
            timespan_1.start_offset, timespan_1.stop_offset,
            timespan_2.start_offset, timespan_2.stop_offset)
        return truth_value

    def __eq__(self, expr):
        r'''Is true when `expr` equals time relation. Otherwise false:

        ::

            >>> timespan = timespantools.Timespan(0, 10)
            >>> time_relation_1 = \
            ...     timespantools.timespan_2_starts_during_timespan_1()
            >>> time_relation_2 = \
            ...     timespantools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)

        ::

            >>> time_relation_1 == time_relation_1
            True
            >>> time_relation_1 == time_relation_2
            False
            >>> time_relation_2 == time_relation_2
            True

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            if self.inequality == expr.inequality:
                if self.timespan_1 == expr.timespan_1:
                    if self.timespan_2 == expr.timespan_2:
                        return True
        return False

    def __hash__(self):
        r'''Hashes time relation.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TimespanTimespanTimeRelation, self).__hash__()

    ### PUBLIC METHODS ###

    def get_counttime_components(self, counttime_components):
        r'''Get `counttime_components` that satisfy `time_relation`:

        ::

            >>> voice = Voice(
            ...     [Note(i % 36, Duration(1, 4)) for i in range(200)])
            >>> timespan_1 = timespantools.Timespan(20, 22)
            >>> time_relation = \
            ...     timespantools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> result = time_relation.get_counttime_components(voice[:])

        ::

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

        ::

            >>> result.get_timespan()
            Timespan(start_offset=Offset(20, 1), stop_offset=Offset(22, 1))

        `counttime_components` must belong to a single voice.

        `counttime_components` must be time-contiguous.

        The call shown here takes 78355 function calls under r9686.

        Returns selection.
        '''
        from abjad.tools import selectiontools
        from abjad.tools import timespantools

        # check input
        assert isinstance(counttime_components, (
            list, selectiontools.Selection)), repr(counttime_components)
        assert self.timespan_1 is not None

        # iterate counttime components
        result = []
        for counttime_component in counttime_components:
            if self(timespan_2=counttime_component._get_timespan()):
                result.append(counttime_component)

        # return result
        return selectiontools.Selection(result)

    def get_offset_indices(
        self, timespan_2_start_offsets, timespan_2_stop_offsets):
        r'''Get offset indices that satisfy time relation:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
            >>> start_offsets = [inspect_(note).get_timespan().start_offset for note in staff]
            >>> stop_offsets = [inspect_(note).get_timespan().stop_offset for note in staff]

        ..  container:: example

            **Example 1.** Notes equal to ``staff[0:2]`` start
            during timespan ``[0, 3/16)``:

            ::

                >>> timespan_1 = timespantools.Timespan(Offset(0), Offset(3, 16))
                >>> time_relation = \
                ...     timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan_1)
                >>> time_relation.get_offset_indices(start_offsets, stop_offsets)
                (0, 2)

        ..  container:: example

            **Example 2.** Notes equal to ``staff[2:8]`` start after timespan
            ``[0, 3/16)`` stops:

            ::

                >>> timespan_1 = timespantools.Timespan(Offset(0), Offset(3, 16))
                >>> time_relation = \
                ...     timespantools.timespan_2_starts_after_timespan_1_stops(
                ...     timespan_1=timespan_1)
                >>> time_relation.get_offset_indices(start_offsets, stop_offsets)
                (2, 8)

        Returns nonnegative integer pair.
        '''
        from abjad.tools import timespantools
        from abjad.tools import timespantools

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
        r'''Is true when `timespan_1` and `timespan_2` are both not none.
        Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> time_relation = \
            ...     timespantools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1,
            ...     timespan_2=timespan_2,
            ...     hold=True,
            ...     )

        ::

            >>> time_relation.is_fully_loaded
            True

        Returns true or false.
        '''
        return self.timespan_1 is not None and self.timespan_2 is not None

    @property
    def is_fully_unloaded(self):
        r'''Is true when `timespan_1` and `timespan_2` are both none.
        Otherwise false.

            >>> time_relation.is_fully_unloaded
            False

        Returns true or false.
        '''
        return self.timespan_1 is None and self.timespan_2 is None

    @property
    def timespan_1(self):
        r'''Time relation timespan ``1``:

        ::

            >>> time_relation.timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Returns timespan.
        '''
        return self._timespan_1

    @property
    def timespan_2(self):
        r'''Time relation timespan ``2``:

        ::

            >>> time_relation.timespan_2
            Timespan(start_offset=Offset(5, 1), stop_offset=Offset(15, 1))

        Returns timespan.
        '''
        return self._timespan_2
