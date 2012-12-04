from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class SingleSourceSymbolicTimespan(SymbolicTimespan):
    r'''.. versionadded 1.0

    Finite timespan defined in terms of a single source.

    SymbolicTimespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    SymbolicTimespan of the entire score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan()
        SingleSourceSymbolicTimespan()

    SymbolicTimespan of the first third of the score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))

    SymbolicTimespan of the first ``1/8`` of a whole note in score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), right_offset=Offset(1, 8))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), right_offset=Offset(1, 8))

    SymbolicTimespan of the last ``1/8`` of a whole note in score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), left_offset=Offset(-1, 8))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), left_offset=Offset(-1, 8))

    SymbolicTimespan of the segment with name ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentTimespanSelector(identifier='red')

    ::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(selector=segment_selector)
        SingleSourceSymbolicTimespan(selector=SingleSegmentTimespanSelector(identifier='red'))

    SymbolicTimespan of the first measure that starts during segment ``'red'``::

        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> measure_selector = symbolictimetools.BackgroundMeasureSymbolicTimespan(time_relation=time_relation, stop_identifier=1)

    ::

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(selector=measure_selector)

    ::

        >>> z(timespan)
        symbolictimetools.SingleSourceSymbolicTimespan(
            selector=symbolictimetools.BackgroundMeasureSymbolicTimespan(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentTimespanSelector(
                            identifier='red'
                            )
                        )
                    ),
                stop_identifier=1
                )
            )

    SymbolicTimespan of division ``0`` starting during segment ``'red'``::

        >>> division_selector = selectortools.DivisionTimespanSelector(time_relation=time_relation, stop_identifier=1)

    ::

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(selector=division_selector)

    ::

       >>> z(timespan)
        symbolictimetools.SingleSourceSymbolicTimespan(
            selector=selectortools.DivisionTimespanSelector(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentTimespanSelector(
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
        >>> segment_slice_selector = selectortools.SegmentTimespanSelector(start_identifier='red', stop_identifier=stop)

    ::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)
        SingleSourceSymbolicTimespan(selector=SegmentTimespanSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1")))

    Timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, multiplier=None, left_offset=None, right_offset=None):
        from experimental import selectortools
        assert isinstance(selector, (selectortools.TimespanSelector, type(None))), repr(selector)
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

        Return multiplier or none.
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
        '''TimespanSelector of symbolic timespan specified by user.

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

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Delegate to ``self.selector.get_offsets()``.

        Return pair.
        '''
        return self.selector.get_offsets(score_specification, context_name)

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.selector.set_segment_identifier()``.
        '''
        return self.selector.set_segment_identifier(segment_identifier)
