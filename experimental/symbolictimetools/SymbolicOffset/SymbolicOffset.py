import fractions
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: merge back to experimental
class SymbolicOffset(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative offset in score.

    Symbolic offset indicating the left edge of score::

        >>> symbolictimetools.SymbolicOffset()
        SymbolicOffset()

    Symbolic offset indicating the right edge of score::

        >>> symbolictimetools.SymbolicOffset(edge=Right)
        SymbolicOffset(edge=Right)

    Symbolic offset ``1/8`` of a whole note into score::

        >>> symbolictimetools.SymbolicOffset(offset=durationtools.Offset(1, 8))
        SymbolicOffset(offset=Offset(1, 8))

    Symbolic offset one third of the way into score::

        >>> symbolictimetools.SymbolicOffset(edge=Right, multiplier=Fraction(1, 3))
        SymbolicOffset(edge=Right, multiplier=Fraction(1, 3))

    Symbolic offset ``1/8`` of a whole note after the first third of score::

        >>> symbolictimetools.SymbolicOffset(edge=Right, multiplier=Fraction(1, 3), offset=durationtools.Offset(1, 8))
        SymbolicOffset(edge=Right, multiplier=Fraction(1, 3), offset=Offset(1, 8))

    Symbolic offset indicating the left edge of segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')

    ::

        >>> symbolictimetools.SymbolicOffset(selector=segment_selector)
        SymbolicOffset(selector=SingleSegmentSelector(identifier='red'))

    Symbolic offset indicating the right edge of segment ``'red'``::

        >>> symbolictimetools.SymbolicOffset(selector=segment_selector, edge=Right)
        SymbolicOffset(selector=SingleSegmentSelector(identifier='red'), edge=Right)

    Symbolic offset indicating ``1/8`` of a whole note after the left edge of
    segment ``'red'``::

        >>> symbolictimetools.SymbolicOffset(selector=segment_selector, offset=durationtools.Offset(1, 8))
        SymbolicOffset(selector=SingleSegmentSelector(identifier='red'), offset=Offset(1, 8))

    Symbolic offset indicating one third of the way into segment ``'red'``::

        >>> symbolictimetools.SymbolicOffset(selector=segment_selector, edge=Right, multiplier=Fraction(1, 3))
        SymbolicOffset(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3))

    Symbolic offset indicating ``1/8`` of a whole note after the right edge of the 
    first third of segment ``'red'``::
    
        >>> symbolictimetools.SymbolicOffset(selector=segment_selector, edge=Right, 
        ... multiplier=Fraction(1, 3), offset=durationtools.Offset(1, 8))
        SymbolicOffset(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3), offset=Offset(1, 8))

    Symbolic offset indicating the left edge of note ``10`` that starts
    during segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> counttime_component_selector = selectortools.CounttimeComponentSelector(
        ... time_relation=time_relation, klass=Note, start_identifier=10, stop_identifier=11)

    ::

        >>> offset = symbolictimetools.SymbolicOffset(selector=counttime_component_selector)

    ::

        >>> z(offset)
        symbolictimetools.SymbolicOffset(
            selector=selectortools.CounttimeComponentSelector(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                klass=notetools.Note,
                start_identifier=10,
                stop_identifier=11
                )
            )

    Timepoint selectors can be arbitrary timespans. This allows recursion into the model.

    Symbolic offset one third of the way into the timespan of segments ``'red'`` through ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSelector(start_identifier='red', stop_identifier=stop)
        >>> timespan = symbolictimetools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)

    ::
    
        >>> offset = symbolictimetools.SymbolicOffset(selector=timespan, edge=Right, multiplier=Fraction(1, 3))

    ::
    
        >>> z(offset)
        symbolictimetools.SymbolicOffset(
            selector=symbolictimetools.SingleSourceSymbolicTimespan(
                selector=selectortools.SegmentSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1")
                    )
                ),
            edge=Right,
            multiplier=Fraction(1, 3)
            )

    Symbolic offset indicating the right edge of note ``10`` that starts
    during segment ``'red'``::

        >>> offset = symbolictimetools.SymbolicOffset(selector=counttime_component_selector, edge=Right)

    ::

        >>> z(offset)
        symbolictimetools.SymbolicOffset(
            selector=selectortools.CounttimeComponentSelector(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                klass=notetools.Note,
                start_identifier=10,
                stop_identifier=11
                ),
            edge=Right
            )

    Symbolic offsets are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, edge=None, multiplier=None, offset=None): 
        from experimental import selectortools 
        from experimental import symbolictimetools
 
        assert isinstance(selector, (selectortools.Selector, 
            symbolictimetools.SingleSourceSymbolicTimespan, type(None))), repr(selector)
        assert edge in (Left, Right, None), repr(edge)
        assert isinstance(multiplier, (fractions.Fraction, type(None))), repr(multiplier)
        if offset is not None:
            offset = durationtools.Offset(offset)
        assert isinstance(offset, (durationtools.Offset, type(None))), repr(offset)
        self._selector = selector
        self._multiplier = multiplier
        self._edge = edge
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a offset with score object indicator,
        edge and offset all indicating those of `self`.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.selector == other.selector:
            return False
        elif not self.edge == other.edge:
            return False
        elif not self.multiplier == other.multiplier:
            return False
        elif not self.offset == other.offset:
            return False
        else:
            return True

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def offset(self):
        '''Symbolic offset offset specified by user.

            >>> offset.offset is None
            True

        Value of none is interpreted as ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._offset

    @property
    def edge(self):
        '''Symbolic offset edge indicator specified by user.
        
            >>> offset.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def multiplier(self):
        '''Symbolic offset multiplier specified by user.

            >>> offset.multiplier is None
            True

        Value of none is interpreted as ``Fraction(1)``.

        Return fraction or none.
        '''
        return self._multiplier

    @property
    def selector(self):
        '''Symbolic offset selector specified by user.
        
            >>> z(offset.selector)
            selectortools.CounttimeComponentSelector(
                time_relation=timerelationtools.TimespanTimespanTimeRelation(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                        selector=selectortools.SingleSegmentSelector(
                            identifier='red'
                            )
                        )
                    ),
                klass=notetools.Note,
                start_identifier=10,
                stop_identifier=11
                )

        Value of none is taken equal the entire score.

        Return selector or none.
        '''
        return self._selector

    @property
    def start_segment_identifier(self):
        '''Symbolic offset start segment identifier.

            >>> offset.start_segment_identifier
            'red'

        Delegate to ``self.selector.start_segment_identifier``.

        Return string or none.
        '''
        return self.selector.start_segment_identifier

    @property
    def stop_segment_identifier(self):
        '''Symbolic offset stop segment identifier.

            >>> offset.stop_segment_identifier
            SegmentIdentifierExpression("'red' + 1")

        Delegate to ``self.selector.stop_segment_identifier``.

        Return string or none.
        '''
        return self.selector.stop_segment_identifier

    ### PUBLIC METHODS ###

    def get_score_offset(self, score_specification, context_name):
        '''Evaluate score offset of symbolic offset when applied
        to `context_name` in `score_specification`.

        .. note:: add example.

        Return offset.
        '''
        edge = self.edge or Left
        start_offset, stop_offset = self.selector.get_offsets(score_specification, context_name)
        if edge == Left:
            score_offset = start_offset
        else:
            score_offset = stop_offset
        multiplier = self.multiplier or fractions.Fraction(1)
        score_offset = multiplier * score_offset
        offset = self.offset or durationtools.Offset(0)
        score_offset = score_offset + offset
        return score_offset
