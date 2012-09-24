import fractions
from abjad.tools import durationtools
from experimental.timetools.TimeObjectInequality import TimeObjectInequality


class TimespanInequality(TimeObjectInequality):
    r'''.. versionadded:: 1.0

    SymbolicTimespan inequality.

    ::

        >>> from experimental import *

    Test for all objects that start during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(timespan_1=selector)

    ::

        >>> z(timespan_inequality)
        timetools.TimespanInequality(
            'timespan_1.start <= timespan_2.start < timespan_1.stop',
            timespan_1=selectortools.SingleSegmentSelector(
                identifier='red'
                )
            )

    Score for further examples::

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

    Example functions calls using the score above::

        >>> timetools.timespan_2_happens_during_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timetools.timespan_2_intersects_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        True

    ::

        >>> timetools.timespan_2_is_congruent_to_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timetools.timespan_2_overlaps_all_of_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timetools.timespan_2_overlaps_start_of_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        True

    ::

        >>> timetools.timespan_2_overlaps_stop_of_timespan_1(timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timetools.timespan_2_starts_after_timespan_1_starts(timespan_1=last_tuplet, timespan_2=long_note)
        False

    ::

        >>> timetools.timespan_2_starts_after_timespan_1_stops(timespan_1=last_tuplet, timespan_2=long_note)
        False

    SymbolicTimespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, template, timespan_1=None, timespan_2=None):
        TimeObjectInequality.__init__(self, template)
        self._timespan_1 = timespan_1
        self._timespan_2 = timespan_2

    ### SPECIAL METHODS ###

    def __call__(self, timespan_1=None, timespan_2=None):
        r'''Evaluate timespan inequality.

        Example 1. Evaluate timespan inequality without substitution::

            >>> timespan_1 = durationtools.TimespanConstant(5, 15)
            >>> timespan_2 = durationtools.TimespanConstant(10, 20)

        ::

            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1, timespan_2=timespan_2, hold=True)

        ::

            >>> z(timespan_inequality)
            timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=durationtools.TimespanConstant(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(15, 1)
                    ),
                timespan_2=durationtools.TimespanConstant(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                )

        ::

            >>> timespan_inequality()
            True

        Example 2. Substitute `timespan_1` during evaluation::

            >>> new_timespan_1 = timeobjecttools.expr_to_timespan((0, 10))

        ::

            >>> new_timespan_1
            TimespanConstant(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ::

            >>> timespan_inequality(timespan_1=new_timespan_1)
            False

        Example 3. Substitute `timespan_2` during evaluation::

            >>> new_timespan_2 = timeobjecttools.expr_to_timespan((2, 12))

        ::

            >>> new_timespan_2
            TimespanConstant(start_offset=Offset(2, 1), stop_offset=Offset(12, 1))

        ::

            >>> timespan_inequality(timespan_2=new_timespan_2)
            False
        
        Example 4. Substitute both `timespan_1` and `timespan_2` during evaluation::

            >>> timespan_inequality(timespan_1=new_timespan_1, timespan_2=new_timespan_2)
            True

        Raise value error if either `timespan_1` or `timespan_2` is none.

        Otherwise return boolean.
        '''
        from experimental import timeobjecttools
        if timespan_1 is None:
            timespan_1 = self.timespan_1
        if timespan_2 is None:
            timespan_2 = self.timespan_2
        if timespan_1 is None or timespan_2 is None:
            raise ValueError('timespan inequality is not fully loaded.')
        timespan_1 = timeobjecttools.expr_to_timespan(timespan_1)
        timespan_2 = timeobjecttools.expr_to_timespan(timespan_2)
        timespan_1_start = self._get_expr_start(timespan_1)
        timespan_1_stop = self._get_expr_stop(timespan_1)
        timespan_2_start = self._get_expr_start(timespan_2)
        timespan_2_stop = self._get_expr_stop(timespan_2)
        command = self.template
        command = command.replace('timespan_1.start', repr(timespan_1_start))
        command = command.replace('timespan_1.stop', repr(timespan_1_stop))
        command = command.replace('timespan_2.start', repr(timespan_2_start))
        command = command.replace('timespan_2.stop', repr(timespan_2_stop))
        #self._debug(command, 'command')
        result = eval(command, {'Offset': durationtools.Offset})
        return result
    
    def __eq__(self, expr):
        '''True when `expr` equals timespan inequality. Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.template == expr.template:
                if self.timespan_1 == expr.timespan_1:
                    if self.timespan_2 == expr.timespan_2:
                        return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan_1(self):
        '''Expression ``1`` of timespan inequality.

        Return arbitrary object.
        '''
        return self._timespan_1
        
    @property
    def timespan_2(self):
        '''Expression ``2`` of timespan inequality.

        Return arbitrary object.
        '''
        return self._timespan_2
        
    @property
    def is_fully_loaded(self):
        '''True when `timespan_1` and `timespan_2` are both not none.
        Otherwise false.

        Return boolean.
        '''
        return self.timespan_1 is not None and self.timespan_2 is not None

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.timespan.start_segment_identifier``.
        '''
        return self.timespan.start_segment_identifier

    @property
    def stop_segment_identifier(self):
        '''Delegate to ``self.timespan.stop_segment_identifier``.
        '''
        return self.timespan.stop_segment_identifier

    # TODO: eventually remove in favor of timespan_1
    @property
    def timespan(self):
        '''SymbolicTimespan of timespan inequality.

        Return timespan object.
        '''
        #return self._timespan
        return self._timespan_1

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        '''Delegate to ``self.timespan_1.get_duration()``.
        '''
        return self.timespan_1.get_duration(score_specification, context_name)

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.timespan_1.set_segment_identifier()``.
        '''
        self.timespan_1.set_segment_identifier(segment_identifier)
