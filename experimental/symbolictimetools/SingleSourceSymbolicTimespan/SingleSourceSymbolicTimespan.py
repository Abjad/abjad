from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class SingleSourceSymbolicTimespan(SymbolicTimespan):
    r'''.. versionadded 1.0

    Finite timespan defined in terms of a single source.

    Symbolic timespan objects highlight a contiguous blocks of time
    somewhere and say "everything within my bounds is selected
    for some upcoming operation."

    Symbolic timespan of the entire score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan()
        SingleSourceSymbolicTimespan()

    Symbolic timespan of the first third of the score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(1, 3))

    Symbolic timespan of the first ``1/8`` of a whole note in score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), right_offset=Offset(1, 8))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), right_offset=Offset(1, 8))

    Symbolic timespan of the last ``1/8`` of a whole note in score::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), left_offset=Offset(-1, 8))
        SingleSourceSymbolicTimespan(multiplier=Multiplier(0, 1), left_offset=Offset(-1, 8))

    Symbolic timespan of the segment with name ``'red'``::

        >>> segment_selector = symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')

    ::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(selector=segment_selector)
        SingleSourceSymbolicTimespan(selector=SingleSegmentSymbolicTimespan(identifier='red'))

    Symbolic timespan of the first measure that starts during segment ``'red'``::

        >>> measure = symbolictimetools.BackgroundMeasureSymbolicTimespan(anchor='red', stop_identifier=1)

    ::

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(selector=measure)

    ::

        >>> z(timespan)
        symbolictimetools.SingleSourceSymbolicTimespan(
            selector=symbolictimetools.BackgroundMeasureSymbolicTimespan(
                anchor='red',
                stop_identifier=1
                )
            )

    Symbolic timespan of voice ``1`` division ``0`` that starts during segment ``'red'``::

        >>> division = symbolictimetools.DivisionSymbolicTimespan(
        ... anchor='red', stop_identifier=1, voice_name='Voice 1')

    ::

        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(selector=division)

    ::

       >>> z(timespan)
        symbolictimetools.SingleSourceSymbolicTimespan(
            selector=symbolictimetools.DivisionSymbolicTimespan(
                anchor='red',
                stop_identifier=1,
                voice_name='Voice 1'
                )
            )

    SymbolicTimespan starting at the left edge of the segment with the name ``'red'``
    and stopping at the right edge of the segment with the name ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segments = symbolictimetools.SegmentSymbolicTimespan(start_identifier='red', stop_identifier=stop)

    ::

        >>> symbolictimetools.SingleSourceSymbolicTimespan(selector=segments)
        SingleSourceSymbolicTimespan(selector=SegmentSymbolicTimespan(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'blue' + 1")))

    Timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, multiplier=None, left_offset=None, right_offset=None):
        from experimental import symbolictimetools
        assert isinstance(selector, (symbolictimetools.TimespanSymbolicTimespan, type(None))), repr(selector)
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
        '''TimespanSymbolicTimespan of symbolic timespan specified by user.

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
