from abjad.tools import durationtools
from abjad.tools.timerelationtools.TimeRelation import TimeRelation


class TimespanTimespanTimeRelation(TimeRelation):
    r'''.. versionadded:: 2.11

    Timespan / timespan time relation.

    Score for examples:

    ::

        >>> staff_1 = Staff(r"\times 2/3 { c'4 d'4 e'4 } \times 2/3 { f'4 g'4 a'4 }")
        >>> staff_2 = Staff("c'2. d'4")
        >>> score = Score([staff_1, staff_2])

    ::

        >>> f(score)
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

    Example functions calls using the score above:

    ::

        >>> timerelationtools.timespan_2_happens_during_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timerelationtools.timespan_2_intersects_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        True

    ::

        >>> timerelationtools.timespan_2_is_congruent_to_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timerelationtools.timespan_2_overlaps_all_of_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timerelationtools.timespan_2_overlaps_start_of_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        True

    ::

        >>> timerelationtools.timespan_2_overlaps_stop_of_timespan_1(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timerelationtools.timespan_2_starts_after_timespan_1_starts(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timerelationtools.timespan_2_starts_after_timespan_1_stops(
        ... timespan_1=last_tuplet, timespan_2=long_note)
        False

    Timespan / timespan time relations are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequalities, timespan_1=None, timespan_2=None):
        TimeRelation.__init__(self, None, inequalities)
        self._timespan_1 = timespan_1
        self._timespan_2 = timespan_2

    ### SPECIAL METHODS ###

    # TODO: test and see if context_name=None can be removed entirely.
    # TODO: streamline this entire method to delegate evaluation to SimpleInequality, CompoundInequality
    def __call__(self, timespan_1=None, timespan_2=None, score_specification=None, context_name=None):
        r'''Evaluate time relation.

        Example 1. Evaluate time relation without substitution:

        ::

            >>> timespan_1 = timespantools.Timespan(5, 15)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1, timespan_2=timespan_2, hold=True)

        ::

            >>> z(time_relation)
            timerelationtools.TimespanTimespanTimeRelation(
                timerelationtools.CompoundInequality([
                    'timespan_1.start_offset <= timespan_2.start_offset',
                    'timespan_2.start_offset < timespan_1.stop_offset'
                    ],
                    logical_operator='and'
                    ),
                timespan_1=timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(15, 1)
                    ),
                timespan_2=timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                )

        ::

            >>> time_relation()
            True

        Example 2. Substitute `timespan_1` during evaluation:

        ::

            >>> new_timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> new_timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ::

            >>> time_relation(timespan_1=new_timespan_1)
            False

        Example 3. Substitute `timespan_2` during evaluation:

        ::

            >>> new_timespan_2 = timespantools.Timespan(2, 12)

        ::

            >>> new_timespan_2
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(12, 1))

        ::

            >>> time_relation(timespan_2=new_timespan_2)
            False

        Example 4. Substitute both `timespan_1` and `timespan_2` during evaluation:

        ::

            >>> time_relation(timespan_1=new_timespan_1, timespan_2=new_timespan_2)
            True

        Raise value error if either `timespan_1` or `timespan_2` is none.

        Otherwise return boolean.
        '''
        from abjad.tools import timerelationtools
        from abjad.tools import timespantools
        if timespan_1 is None:
            timespan_1 = self.timespan_1
        if timespan_2 is None:
            timespan_2 = self.timespan_2
        if timespan_1 is None or timespan_2 is None:
            raise ValueError('time relation is not fully loaded: {!r}.'.format(self))
        if not isinstance(timespan_1, timespantools.Timespan):
            timespan_1 = timespantools.Timespan()._get_timespan(timespan_1)
        if not isinstance(timespan_2, timespantools.Timespan):
            timespan_2 = timespantools.Timespan()._get_timespan(timespan_2)
        timespan_1_start_offset, timespan_1_stop_offset = self._get_expr_offsets(
            timespan_1, score_specification=score_specification, context_name=context_name)
        timespan_2_start_offset, timespan_2_stop_offset = self._get_expr_offsets(
            timespan_2, score_specification=score_specification, context_name=context_name)
        if not isinstance(self.inequalities, timerelationtools.CompoundInequality):
            truth_values = []
            for inequality in self.inequalities:
                inequality = inequality.replace('timespan_1.start_offset', repr(timespan_1_start_offset))
                inequality = inequality.replace('timespan_1.stop_offset', repr(timespan_1_stop_offset))
                inequality = inequality.replace('timespan_2.start_offset', repr(timespan_2_start_offset))
                inequality = inequality.replace('timespan_2.stop_offset', repr(timespan_2_stop_offset))
                truth_value = eval(inequality, {'Offset': durationtools.Offset})
                truth_values.append(truth_value)
            truth_value = all(truth_values)
        else:
            truth_value = self.inequalities.evaluate(
                timespan_1_start_offset, timespan_1_stop_offset, 
                timespan_2_start_offset, timespan_2_stop_offset)
        return truth_value

    def __eq__(self, expr):
        '''True when `expr` equals time relation. Otherwise false:

        ::

            >>> timespan = timespantools.Timespan(0, 10)
            >>> time_relation_1 = timerelationtools.timespan_2_starts_during_timespan_1()
            >>> time_relation_2 = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)

        ::

            >>> time_relation_1 == time_relation_1
            True
            >>> time_relation_1 == time_relation_2
            False
            >>> time_relation_2 == time_relation_2
            True

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.inequalities == expr.inequalities:
                if self.timespan_1 == expr.timespan_1:
                    if self.timespan_2 == expr.timespan_2:
                        return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_fully_loaded(self):
        '''True when `timespan_1` and `timespan_2` are both not none.
        Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1, timespan_2=timespan_2, hold=True)

        ::

            >>> time_relation.is_fully_loaded
            True

        Return boolean.
        '''
        return self.timespan_1 is not None and self.timespan_2 is not None

    @property
    def is_fully_unloaded(self):
        '''True when `timespan_1` and `timespan_2` are both none.
        Otherwise false.

            >>> time_relation.is_fully_unloaded
            False

        Return boolean.
        '''
        return self.timespan_1 is None and self.timespan_2 is None

    @property
    def timespan_1(self):
        '''Time relation timespan ``1``:

        ::

            >>> time_relation.timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Return timespan.
        '''
        return self._timespan_1

    @property
    def timespan_2(self):
        '''Time relation timespan ``2``:

        ::

            >>> time_relation.timespan_2
            Timespan(start_offset=Offset(5, 1), stop_offset=Offset(15, 1))

        Return timespan.
        '''
        return self._timespan_2
