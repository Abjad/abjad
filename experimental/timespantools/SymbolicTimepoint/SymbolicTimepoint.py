import fractions
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimepoint(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    Symbolic timepoint indicating the left edge of score::

        >>> from experimental import *

    ::

        >>> timespantools.SymbolicTimepoint()
        SymbolicTimepoint()

    Symbolic timepoint indicating the right edge of score::

        >>> timespantools.SymbolicTimepoint(edge=Right)
        SymbolicTimepoint(edge=Right)

    Symbolic timepoint ``1/8`` of a whole note into score::

        >>> timespantools.SymbolicTimepoint(addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(addendum=Offset(1, 8))

    Symbolic timepoint one third of the way into score::

        >>> timespantools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))

    Symbolic timepoint ``1/8`` of a whole note after the first third of score::

        >>> timespantools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    Symbolic timepoint indicating the left edge of segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')

    ::

        >>> timespantools.SymbolicTimepoint(selector=segment_selector)
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'))

    Symbolic timepoint indicating the right edge of segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(selector=segment_selector, edge=Right)
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right)

    Symbolic timepoint indicating ``1/8`` of a whole note after the left edge of
    segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(selector=segment_selector, addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), addendum=Offset(1, 8))

    Symbolic timepoint indicating one third of the way into segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(selector=segment_selector, edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3))

    Symbolic timepoint indicating ``1/8`` of a whole note after the right edge of the 
    first third of segment ``'red'``::
    
        >>> timespantools.SymbolicTimepoint(selector=segment_selector, edge=Right, 
        ... multiplier=Fraction(1, 3), addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(selector=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    Symbolic timepoint indicating the left edge of note ``10`` that starts
    during segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> inequality = timespaninequalitytools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> counttime_component_selector = selectortools.CounttimeComponentSelector(
        ... inequality=inequality, klass=Note, start_identifier=10, stop_identifier=11)

    ::

        >>> timepoint = timespantools.SymbolicTimepoint(selector=counttime_component_selector)

    ::

        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            selector=selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timespantools.SingleSourceSymbolicTimespan(
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
        >>> timespan = timespantools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)

    ::
    
        >>> timepoint = timespantools.SymbolicTimepoint(selector=timespan, edge=Right, multiplier=Fraction(1, 3))

    ::
    
        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            selector=timespantools.SingleSourceSymbolicTimespan(
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

        >>> timepoint = timespantools.SymbolicTimepoint(selector=counttime_component_selector, edge=Right)

    ::

        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            selector=selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timespantools.SingleSourceSymbolicTimespan(
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

    def __init__(self, selector=None, edge=None, multiplier=None, addendum=None): 
        from experimental import selectortools 
        from experimental import timespantools 
        assert isinstance(selector, 
            (selectortools.Selector, timespantools.SingleSourceSymbolicTimespan, type(None))), repr(selector)
        assert edge in (Left, Right, None), repr(edge)
        assert isinstance(multiplier, (fractions.Fraction, type(None))), repr(multiplier)
        if addendum is not None:
            addendum = durationtools.Offset(addendum)
        assert isinstance(addendum, (durationtools.Offset, type(None))), repr(addendum)
        self._selector = selector
        self._multiplier = multiplier
        self._edge = edge
        self._addendum = addendum

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
        elif not self.addendum == other.addendum:
            return False
        else:
            return True

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addendum(self):
        '''Symbolic timepoint addendum specified by user.

            >>> timepoint.addendum is None
            True

        Value of none is interpreted as ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._addendum

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
    def segment_identifier(self):
        '''Delegate to ``self.selector.segment_identifier``.

            >>> timepoint.segment_identifier
            'red'

        Return string or none.
        '''
        return self.selector.segment_identifier

    @property
    def selector(self):
        '''Symbolic timepoint selector specified by user.
        
            >>> z(timepoint.selector)
            selectortools.CounttimeComponentSelector(
                inequality=timespaninequalitytools.TimespanInequality(
                    'timespan_1.start <= timespan_2.start < timespan_1.stop',
                    timespan_1=timespantools.SingleSourceSymbolicTimespan(
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
        addendum = self.addendum or durationtools.Offset(0)
        segment_offset = segment_offset + addendum
        return segment_offset
