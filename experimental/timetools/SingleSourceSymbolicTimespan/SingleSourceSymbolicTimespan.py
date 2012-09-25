from experimental.timetools.SymbolicTimespan import SymbolicTimespan


class SingleSourceSymbolicTimespan(SymbolicTimespan):
    r'''.. versionadded 1.0

    Finite timespan defined in terms of a single source.

    SymbolicTimespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation." ::

        >>> from experimental import *

    SymbolicTimespan of the entire score::

        >>> timetools.SingleSourceSymbolicTimespan()
        SingleSourceSymbolicTimespan()

    SymbolicTimespan of the first third of the score::

        >>> timetools.SingleSourceSymbolicTimespan(multiplier=Fraction(1, 3))
        SingleSourceSymbolicTimespan(multiplier=Fraction(1, 3))

    SymbolicTimespan of the first ``1/8`` of a whole note in score::

        >>> timetools.SingleSourceSymbolicTimespan(multiplier=Fraction(0, 1), right_offset=durationtools.Offset(1, 8))
        SingleSourceSymbolicTimespan(multiplier=Fraction(0, 1), right_offset=Offset(1, 8))

    SymbolicTimespan of the last ``1/8`` of a whole note in score::

        >>> timetools.SingleSourceSymbolicTimespan(multiplier=Fraction(0, 1), left_offset=durationtools.Offset(-1, 8))
        SingleSourceSymbolicTimespan(multiplier=Fraction(0, 1), left_offset=Offset(-1, 8))

    SymbolicTimespan of the segment with name ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')

    ::

        >>> timetools.SingleSourceSymbolicTimespan(selector=segment_selector)
        SingleSourceSymbolicTimespan(selector=SingleSegmentSelector(identifier='red'))

    SymbolicTimespan of the first measure that starts during segment ``'red'``::

        >>> inequality = timetools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> measure_selector = selectortools.BackgroundMeasureSelector(inequality=inequality, stop_identifier=1)

    ::

        >>> timespan = timetools.SingleSourceSymbolicTimespan(selector=measure_selector)

    ::

        >>> z(timespan)
        timetools.SingleSourceSymbolicTimespan(
            selector=selectortools.BackgroundMeasureSelector(
                inequality=timetools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=1
                )
            )

    SymbolicTimespan of division ``0`` starting during segment ``'red'``::

        >>> division_selector = selectortools.DivisionSelector(inequality=inequality, stop_identifier=1)

    ::

        >>> timespan = timetools.SingleSourceSymbolicTimespan(selector=division_selector)

    ::

       >>> z(timespan)
        timetools.SingleSourceSymbolicTimespan(
            selector=selectortools.DivisionSelector(
                inequality=timetools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=1
                )
            )

    SymbolicTimespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSelector(start_identifier='red', stop_identifier=stop)

    ::

        >>> timetools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)
        SingleSourceSymbolicTimespan(selector=SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1")))

    Timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, multiplier=None, left_offset=None, right_offset=None):
        from experimental import selectortools
        assert isinstance(selector, (selectortools.Selector, type(None))), repr(selector)
        SymbolicTimespan.__init__(self)
        self._selector = selector
        self._multiplier = multiplier
        self._left_offset = left_offset
        self._right_offset = right_offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` equals self. Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.selector == expr.selector:
                if self.multiplier == expr.multiplier:
                    if self.left_offset == expr.left_offset:
                        if self.right_offset == expr.right_offset:
                            return True
        return False
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def left_offset(self):
        '''Left offset of symbolic timespan specified by user.

        Return offset or none.
        '''
        return self._left_offset

    @property
    def multiplier(self):
        '''Multiplier of symbolic timespan specified by user.

        Return fraction or none.
        '''
        return self._multiplier
    
    @property
    def right_offset(self):
        '''Right offset of symbolic timespan specified by user.

        Return offset or none.
        '''
        return self._right_offset

    @property
    def selector(self):
        '''Selector of symbolic timespan specified by user.

        Return selector or none.
        '''
        return self._selector

    @property
    def start_segment_identifier(self):
        '''Start segment identifier of symbolic timespan specified by user.

        Delegate to ``self.selector.start_segment_identifier``.

        Return string or integer.
        '''
        return self.selector.start_segment_identifier

    @property
    def stop_segment_identifier(self):
        '''Start segment identifier of symbolic timespan specified by user.

        Delegate to ``self.selector.stop_segment_identifier``.

        Return string or integer.
        '''
        return self.selector.stop_segment_identifier
    
    ### PUBLIC METHODS ###

    def get_score_start_offset(self, score_specification, context_name):
        '''Evaluate score start offset of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Delegate to ``self.selector.get_score_start_offset()``.

        Return offset.
        '''
        return self.selector.get_score_start_offset(score_specification, context_name)

    def get_score_stop_offset(self, score_specification, context_name):
        '''Evaluate score stop offset of symbolic timespan when applied
        to `context_name` in `score_specification`.
        
        Delegate to ``self.selector.get_score_stop_offset()``.

        Return offset.
        '''
        return self.selector.get_score_stop_offset(score_specification, context_name)

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.selector.set_segment_identifier()``.
        '''
        return self.selector.set_segment_identifier(segment_identifier)
