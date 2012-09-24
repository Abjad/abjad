import fractions
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimepoint(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    Symbolic timepoint indicating the left edge of score::

        >>> from experimental import *

    ::

        >>> timeobjecttools.SymbolicTimepoint()
        SymbolicTimepoint()

    Symbolic timepoint indicating the right edge of score::

        >>> timeobjecttools.SymbolicTimepoint(edge=Right)
        SymbolicTimepoint(edge=Right)

    Symbolic timepoint ``1/8`` of a whole note into score::

        >>> timeobjecttools.SymbolicTimepoint(offset=durationtools.Offset(1, 8))
        SymbolicTimepoint(offset=Offset(1, 8))

    Symbolic timepoint one third of the way into score::

        >>> timeobjecttools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))

    Symbolic timepoint ``1/8`` of a whole note after the first third of score::

        >>> timeobjecttools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), offset=durationtools.Offset(1, 8))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), offset=Offset(1, 8))

    Symbolic timepoint indicating the left edge of segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')

    ::

        >>> timeobjecttools.SymbolicTimepoint(selector=segment_selector)
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'))

    Symbolic timepoint indicating the right edge of segment ``'red'``::

        >>> timeobjecttools.SymbolicTimepoint(selector=segment_selector, edge=Right)
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right)

    Symbolic timepoint indicating ``1/8`` of a whole note after the left edge of
    segment ``'red'``::

        >>> timeobjecttools.SymbolicTimepoint(selector=segment_selector, offset=durationtools.Offset(1, 8))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), offset=Offset(1, 8))

    Symbolic timepoint indicating one third of the way into segment ``'red'``::

        >>> timeobjecttools.SymbolicTimepoint(selector=segment_selector, edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3))

    Symbolic timepoint indicating ``1/8`` of a whole note after the right edge of the 
    first third of segment ``'red'``::
    
        >>> timeobjecttools.SymbolicTimepoint(selector=segment_selector, edge=Right, 
        ... multiplier=Fraction(1, 3), offset=durationtools.Offset(1, 8))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3), offset=Offset(1, 8))

    Symbolic timepoint indicating the left edge of note ``10`` that starts
    during segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> inequality = timespaninequalitytools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> counttime_component_selector = selectortools.CounttimeComponentSelector(
        ... inequality=inequality, klass=Note, start_identifier=10, stop_identifier=11)

    ::

        >>> timepoint = timeobjecttools.SymbolicTimepoint(selector=counttime_component_selector)

    ::

        >>> z(timepoint)
        timeobjecttools.SymbolicTimepoint(
            selector=selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timeobjecttools.SingleSourceSymbolicTimespan(
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

    Symbolic timepoint one third of the way into the timespan of segments ``'red'`` through ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSelector(start_identifier='red', stop_identifier=stop)
        >>> timespan = timeobjecttools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)

    ::
    
        >>> timepoint = timeobjecttools.SymbolicTimepoint(selector=timespan, edge=Right, multiplier=Fraction(1, 3))

    ::
    
        >>> z(timepoint)
        timeobjecttools.SymbolicTimepoint(
            selector=timeobjecttools.SingleSourceSymbolicTimespan(
                selector=selectortools.SegmentSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1")
                    )
                ),
            edge=Right,
            multiplier=Fraction(1, 3)
            )

    Symbolic timepoint indicating the right edge of note ``10`` that starts
    during segment ``'red'``::

        >>> timepoint = timeobjecttools.SymbolicTimepoint(selector=counttime_component_selector, edge=Right)

    ::

        >>> z(timepoint)
        timeobjecttools.SymbolicTimepoint(
            selector=selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timeobjecttools.SingleSourceSymbolicTimespan(
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

    Symbolic timepoints are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, edge=None, multiplier=None, offset=None): 
        from experimental import selectortools 
        from experimental import timeobjecttools 
        assert isinstance(selector, 
            (selectortools.Selector, timeobjecttools.SingleSourceSymbolicTimespan, type(None))), repr(selector)
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
        '''True when `other` is a timepoint with score object indicator,
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
        '''Symbolic timepoint offset specified by user.

            >>> timepoint.offset is None
            True

        Value of none is interpreted as ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._offset

    @property
    def edge(self):
        '''Symbolic timepoint edge indicator specified by user.
        
            >>> timepoint.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def multiplier(self):
        '''Symbolic timepoint multiplier specified by user.

            >>> timepoint.multiplier is None
            True

        Value of none is interpreted as ``Fraction(1)``.

        Return fraction or none.
        '''
        return self._multiplier

    @property
    def selector(self):
        '''Symbolic timepoint selector specified by user.
        
            >>> z(timepoint.selector)
            selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timeobjecttools.SingleSourceSymbolicTimespan(
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
        '''Symbolic timepoint start segment identifier.

            >>> timepoint.start_segment_identifier
            'red'

        Delegate to ``self.selector.start_segment_identifier``.

        Return string or none.
        '''
        return self.selector.start_segment_identifier

    @property
    def stop_segment_identifier(self):
        '''Symbolic timepoint stop segment identifier.

            >>> timepoint.stop_segment_identifier
            SegmentIdentifierExpression("'red' + 1")

        Delegate to ``self.selector.stop_segment_identifier``.

        Return string or none.
        '''
        return self.selector.stop_segment_identifier

    ### PUBLIC METHODS ###

    def get_score_offset(self, score_specification):
        '''Evaluate score offset of symbolic timepoint when applied
        to `score_specification`.

        .. note:: not yet implemented.

        Return offset.
        '''
        raise NotImplementedError

    def get_segment_offset(self, score_specification, context_name):
        '''Evaluate segment offset of symbolic timepoint when applied
        to `score_specification`.

        Return offset.
        '''
        edge = self.edge or Left
        if edge == Left:
            segment_offset = self.selector.get_segment_start_offset(score_specification, context_name)
        else:
            segment_offset = self.selector.get_segment_stop_offset(score_specification, context_name)
        multiplier = self.multiplier or fractions.Fraction(1)     
        segment_offset = multiplier * segment_offset
        offset = self.offset or durationtools.Offset(0)
        segment_offset = segment_offset + offset
        return segment_offset
