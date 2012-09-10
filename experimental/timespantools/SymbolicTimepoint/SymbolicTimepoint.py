import fractions
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimepoint(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    SymbolicTimepoint equal to the left edge of score::

        >>> from experimental import *

    ::

        >>> timespantools.SymbolicTimepoint()
        SymbolicTimepoint()

    SymbolicTimepoint equal to the right edge of score::

        >>> timespantools.SymbolicTimepoint(edge=Right)
        SymbolicTimepoint(edge=Right)

    SymbolicTimepoint ``1/8`` of a whole note into score::

        >>> timespantools.SymbolicTimepoint(addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(addendum=Offset(1, 8))

    SymbolicTimepoint one third of the way into score::

        >>> timespantools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3))

    SymbolicTimepoint ``1/8`` of a whole note after the first third of score::

        >>> timespantools.SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    SymbolicTimepoint equal to the left edge of segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')

    ::

        >>> timespantools.SymbolicTimepoint(anchor=segment_selector)
        SymbolicTimepoint(anchor=SingleSegmentSelector(identifier='red'))

    SymbolicTimepoint equal to the right edge of segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(anchor=segment_selector, edge=Right)
        SymbolicTimepoint(anchor=SingleSegmentSelector(identifier='red'), edge=Right)

    SymbolicTimepoint equal to ``1/8`` of a whole note after the left edge of
    segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(anchor=segment_selector, addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(anchor=SingleSegmentSelector(identifier='red'), addendum=Offset(1, 8))

    SymbolicTimepoint equal to one third of the way into segment ``'red'``::

        >>> timespantools.SymbolicTimepoint(anchor=segment_selector, edge=Right, multiplier=Fraction(1, 3))
        SymbolicTimepoint(anchor=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3))

    SymbolicTimepoint equal to ``1/8`` of a whole note after the right edge of the 
    first third of segment ``'red'``::
    
        >>> timespantools.SymbolicTimepoint(anchor=segment_selector, edge=Right, 
        ... multiplier=Fraction(1, 3), addendum=durationtools.Offset(1, 8))
        SymbolicTimepoint(anchor=SingleSegmentSelector(identifier='red'), edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    SymbolicTimepoint equal to the left edge of note ``10`` that starts
    during segment ``'red'``::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> inequality = timespaninequalitytools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)
        >>> counttime_component_selector = selectortools.CounttimeComponentSelector(
        ... inequality=inequality, klass=Note, start_identifier=10, stop_identifier=11)

    ::

        >>> timepoint = timespantools.SymbolicTimepoint(anchor=counttime_component_selector)

    ::

        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            anchor=selectortools.CounttimeComponentSelector(
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

    Timepoints can anchor to arbitrary timespans. This allows recursion into the model.

    SymbolicTimepoint one third of the way into the timespan of segments ``'red'`` through ``'blue'``::

        >>> stop = helpertools.SegmentIdentifierExpression("'blue' + 1")
        >>> segment_slice_selector = selectortools.SegmentSelector(start_identifier='red', stop_identifier=stop)
        >>> timespan = timespantools.SingleSourceSymbolicTimespan(selector=segment_slice_selector)

    ::
    
        >>> timepoint = timespantools.SymbolicTimepoint(anchor=timespan, edge=Right, multiplier=Fraction(1, 3))

    ::
    
        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            anchor=timespantools.SingleSourceSymbolicTimespan(
                selector=selectortools.SegmentSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'blue' + 1")
                    )
                ),
            edge=Right,
            multiplier=Fraction(1, 3)
            )

    SymbolicTimepoint equal to the right edge of note ``10`` that starts
    during segment ``'red'``::

        >>> timepoint = timespantools.SymbolicTimepoint(anchor=counttime_component_selector, edge=Right)

    ::

        >>> z(timepoint)
        timespantools.SymbolicTimepoint(
            anchor=selectortools.CounttimeComponentSelector(
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

    Timepoints are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, multiplier=None, addendum=None): 
        from experimental import selectortools 
        from experimental import timespantools 
        assert isinstance(
            anchor, (selectortools.Selector, timespantools.SingleSourceSymbolicTimespan, type(None))), repr(anchor)
        assert edge in (Left, Right, None), repr(edge)
        assert isinstance(multiplier, (fractions.Fraction, type(None))), repr(multiplier)
        if addendum is not None:
            addendum = durationtools.Offset(addendum)
        assert isinstance(addendum, (durationtools.Offset, type(None))), repr(addendum)
        self._anchor = anchor
        self._multiplier = multiplier
        self._edge = edge
        self._addendum = addendum

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a timepoint with score object indicator,
        edge and offset all equal to those of `self`.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.anchor == other.anchor:
            return False
        elif not self.edge == other.edge:
            return False
        elif not self.multiplier == other.multiplier:
            return False
        elif not self.addendum == other.addendum:
            return False
        else:
            return True

    def __ge__(self, other):
        '''.. note:: not yet implemented.
        '''
        if isinstance(other, type(self)):
            return self >= other
        return False

    def __gt__(self, other):
        '''.. note:: not yet implemented.
        '''
        if isinstance(other, type(self)):
            return self > other
        return False

    def __le__(self, other):
        '''.. note:: not yet implemented.
        '''
        if isinstance(other, type(self)):
            return self <= other
        return False

    def __lt__(self, other):
        '''.. note:: not yet implemented.
        '''
        if isinstance(other, type(self)):
            return self < other
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addendum(self):
        '''SymbolicTimepoint addendum specified by user.

            >>> timepoint.addendum is None
            True

        Value of none is interpreted as ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._addendum

    @property
    def anchor(self):
        '''SymbolicTimepoint anchor specified by user.
        
            >>> z(timepoint.anchor)
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
        return self._anchor

    @property
    def edge(self):
        '''SymbolicTimepoint edge indicator specified by user.
        
            >>> timepoint.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def multiplier(self):
        '''SymbolicTimepoint multiplier specified by user.

            >>> timepoint.multiplier is None
            True

        Value of none is interpreted as ``Fraction(1)``.

        Return fraction or none.
        '''
        return self._multiplier

    @property
    def score_offset(self):
        '''Rational-valued offset of timepoint in score.

        Derived from input values.
    
        Return offset.

        .. note:: not yet implemented.

        .. note:: will probably have to be implemented as method intead of property.
        '''
        raise NotImplementedError
