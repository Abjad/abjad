from abjad.tools import componenttools
from abjad.tools import mathtools
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan


class SingleSourceTimespan(Timespan):
    r'''.. versionadded 1.0

    Finite timespan defined in terms of a single source.

    Timespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation." ::

        >>> from experimental import *

    Timespan of the entire score::

        >>> timespantools.SingleSourceTimespan()
        SingleSourceTimespan()

    Timespan of the first third of the score::

        >>> timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
        SingleSourceTimespan(multiplier=Fraction(1, 3))

    Timespan of the first ``1/8`` of a whole note in score::

        >>> timespantools.SingleSourceTimespan(multiplier=Fraction(0, 1), right_addendum=durationtools.Offset(1, 8))
        SingleSourceTimespan(multiplier=Fraction(0, 1), right_addendum=Offset(1, 8))

    Timespan of the last ``1/8`` of a whole note in score::

        >>> timespantools.SingleSourceTimespan(multiplier=Fraction(0, 1), left_addendum=durationtools.Offset(-1, 8))
        SingleSourceTimespan(multiplier=Fraction(0, 1), left_addendum=Offset(-1, 8))

    Timespan of the segment with name ``'red'``::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')

    ::

        >>> timespantools.SingleSourceTimespan(selector=segment_selector)
        SingleSourceTimespan(selector=SegmentItemSelector(identifier='red'))

    Timespan of the first measure that starts during segment ``'red'``::

        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, stop_identifier=1)

    ::

        >>> timespan = timespantools.SingleSourceTimespan(selector=measure_selector)

    ::

        >>> z(timespan)
        timespantools.SingleSourceTimespan(
            selector=selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=1
                )
            )

    Timespan of division ``0`` starting during segment ``'red'``::

        >>> division_selector = selectortools.DivisionSliceSelector(inequality=inequality, stop_identifier=1)

    ::

        >>> timespan = timespantools.SingleSourceTimespan(selector=division_selector)

    ::

       >>> z(timespan)
        timespantools.SingleSourceTimespan(
            selector=selectortools.DivisionSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=1
                )
            )

    Timespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSliceSelector(start_identifier='red', stop_identifier=stop)

    ::

        >>> timespantools.SingleSourceTimespan(selector=segment_slice_selector)
        SingleSourceTimespan(selector=SegmentSliceSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1")))

    Timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, multiplier=None, left_addendum=None, right_addendum=None):
        from experimental import selectortools
        assert isinstance(selector, (selectortools.Selector, type(None))), repr(selector)
        Timespan.__init__(self)
        self._selector = selector
        self._multiplier = multiplier
        self._left_addendum = left_addendum
        self._right_addendum = right_addendum

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.selector == expr.selector:
                if self.multiplier == expr.multiplier:
                    if self.left_addendum == expr.left_addendum:
                        if self.right_addendum == expr.right_addendum:
                            return True
        return False
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def encompasses_one_object_exactly(self):
        '''.. note:: possible to remove this?
        '''
        if self.multiplier is None:
            if self.left_addendum is None:
                if self.right_addendum is None:
                    return True
        return False

    @property
    def encompasses_one_segment_exactly(self):
        '''True when timespan encompasses one object exactly and when that
        object is a segment. Otherwise false.

        Return boolean.
        '''
        from experimental import selectortools
        if self.encompasses_one_object_exactly:
            if isinstance(self.selector, selectortools.SegmentItemSelector):
                return True
        return False

    @property
    def left_addendum(self):
        return self._left_addendum

    @property
    def multiplier(self):
        return self._multiplier
    
    @property
    def right_addendum(self):
        return self._right_addendum

    @property
    def segment_identifier(self):
        '''Return ``self.selector.segment_identifier``.
        '''
        return self.selector.segment_identifier

    @property
    def selector(self):
        '''Selector specified by user.

        Return selector or none.
        '''
        return self._selector
    
    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        '''Delegate to ``self.selector.get_timespan()``.
        '''
        return self.selector.get_duration(score_specification)

    def get_segment_start_offset(self, score_specification):
        '''Delegate to ``self.selector.get_segment_start_offset()``.
        '''
        return self.selector.get_segment_start_offset(score_specification)

    def get_segment_stop_offset(self, score_specification):
        '''Delegate to ``self.selector.get_segment_stop_offset()``.
        '''
        return self.selector.get_segment_stop_offset(score_specification)
