import fractions
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Timespan inequality.

    ::

        >>> from experimental import *

    Test for all objects that start during segment ``'red'``::

        >>> selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan_inequality = timespaninequalitytools.expr_2_starts_during_expr_1(expr_1=selector)

    ::

        >>> z(timespan_inequality)
        timespaninequalitytools.TimespanInequality(
            'expr_1.start <= expr_2.start < expr_1.stop',
            expr_1=selectortools.SingleSegmentSelector(
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

        >>> timespaninequalitytools.expr_2_happens_during_expr_1(expr_1=last_tuplet, expr_2=long_note)
        False

    ::

        >>> timespaninequalitytools.expr_2_intersects_expr_1(expr_1=last_tuplet, expr_2=long_note)
        True

    ::

        >>> timespaninequalitytools.expr_2_is_congruent_to_expr_1(expr_1=last_tuplet, expr_2=long_note)
        False

    ::

        >>> timespaninequalitytools.expr_2_overlaps_all_of_expr_1(expr_1=last_tuplet, expr_2=long_note)
        False

    ::

        >>> timespaninequalitytools.expr_2_overlaps_start_of_expr_1(expr_1=last_tuplet, expr_2=long_note)
        True

    ::

        >>> timespaninequalitytools.expr_2_overlaps_stop_of_expr_1(expr_1=last_tuplet, expr_2=long_note)
        False

    ::

        >>> timespaninequalitytools.expr_2_starts_after_expr_1_starts(expr_1=last_tuplet, expr_2=long_note)
        False

    ::

        >>> timespaninequalitytools.expr_2_starts_after_expr_1_stops(expr_1=last_tuplet, expr_2=long_note)
        False

    Timespan inequalities are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, template, expr_1=None, expr_2=None):
        assert isinstance(template, str)
        self._template = template
        self._expr_1 = expr_1
        self._expr_2 = expr_2

    ### SPECIAL METHODS ###

    def __call__(self):
        from experimental import timespantools
        if self.is_fully_loaded:
            expr_1 = timespantools.expr_to_timespan(self.expr_1)
            expr_2 = timespantools.expr_to_timespan(self.expr_2)
            expr_1_start = self._get_expr_start(expr_1)
            expr_1_stop = self._get_expr_stop(expr_1)
            expr_2_start = self._get_expr_start(expr_2)
            expr_2_stop = self._get_expr_stop(expr_2)
            command = self.template
            command = command.replace('expr_1.start', repr(expr_1_start))
            command = command.replace('expr_1.stop', repr(expr_1_stop))
            command = command.replace('expr_2.start', repr(expr_2_start))
            command = command.replace('expr_2.stop', repr(expr_2_stop))
            result = eval(command, {'Offset': durationtools.Offset})
            return result
        else:
            raise ValueError
    
    # TODO: remove this and rely on AbjadObject __eq__ testing
    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.template == expr.template:
                if self.expr_1 == expr.expr_1:
                    if self.expr_2 == expr.expr_2:
                        return True
        return False

    ### PRIVATE METHODS ###

    def _get_expr_start(self, expr):
        if hasattr(expr, 'start_offset'):
            return expr.start_offset
        else:
            raise ValueError

    def _get_expr_stop(self, expr):
        if hasattr(expr, 'stop_offset'):
            return expr.stop_offset
        else:
            raise ValueError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def expr_1(self):
        '''Expression ``1`` of timespan inequality.

        Return arbitrary object.
        '''
        return self._expr_1
        
    @property
    def expr_2(self):
        '''Expression ``2`` of timespan inequality.

        Return arbitrary object.
        '''
        return self._expr_2
        
    @property
    def is_fully_loaded(self):
        '''True when `expr_1` and `expr_2` are both not none.
        Otherwise false.

        Return boolean.
        '''
        return self.expr_1 is not None and self.expr_2 is not None

    @property
    def segment_identifier(self):
        '''Delegate to ``self.timespan.segment_identifier``.
        '''
        return self.timespan.segment_identifier

    # TODO: eventually remove in favor of expr_1
    @property
    def timespan(self):
        '''Timespan of timespan inequality.

        Return timespan object.
        '''
        #return self._timespan
        return self._expr_1

    @property
    def template(self):
        '''Template of timespan inequality.

        Return string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        '''Delegate to ``self.expr_1.get_duration()``.
        '''
        return self.expr_1.get_duration(score_specification, context_name)

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.expr_1.set_segment_identifier()``.
        '''
        self.expr_1.set_segment_identifier(segment_identifier)
