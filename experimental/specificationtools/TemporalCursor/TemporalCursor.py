from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
from experimental.specificationtools.VectorConstant import VectorConstant
import fractions


class TemporalCursor(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    (Object-oriented delayed evaluation.)

    Temporal cursors locate timepoints relative to arbitrary objects in score.

    Temporal cursors resolve to a rational-valued score offset.

    Temporal cursors afford the location of timepoints relative to score
    objects that do not yet exist.

    Initialize with different combinations of optional `anchor`, 
    `edge`, `scalar` and `addendum`.

    Pick out the timepoint equal to the left edge of score::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.TemporalCursor()
        TemporalCursor()

    Pick out the timepoint equal to the right edge of score::

        >>> specificationtools.TemporalCursor(edge=right)
        TemporalCursor(edge=right)

    Pick out the timepoint ``1/8`` of a whole note into score::

        >>> from abjad.tools.durationtools.Offset import Offset

    ::

        >>> specificationtools.TemporalCursor(addendum=Offset(1, 8))
        TemporalCursor(addendum=Offset(1, 8))

    Pick out the timepoint one third of the way into score::

        >>> specificationtools.TemporalCursor(edge=right, scalar=Fraction(1, 3))
        TemporalCursor(edge=right, scalar=Fraction(1, 3))

    Pick out the timepoint ``1/8`` of a whole note after the first third of score::

        >>> specificationtools.TemporalCursor(edge=right, scalar=Fraction(1, 3), addendum=Offset(1, 8))
        TemporalCursor(edge=right, scalar=Fraction(1, 3), addendum=Offset(1, 8))

    Pick out the timepoint equal to the left edge of the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red')

    ::

        >>> specificationtools.TemporalCursor(anchor=anchor)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'))

    Pick out the timepoint equal to the right edge of the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, edge=right)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), edge=right)

    Pick out the timepoint equal to ``1/8`` of a whole note after the left edge of 
    the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, addendum=Offset(1, 8))
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), addendum=Offset(1, 8))

    Pick out the timepoint equal to one third of the way into the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, edge=right, scalar=Fraction(1, 3))
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), edge=right, scalar=Fraction(1, 3))

    Pick out the timepoint equal to ``1/8`` of a whole note after the right edge of the first third of
    the segment with name ``'red'``::
    
        >>> specificationtools.TemporalCursor(anchor=anchor, edge=right, scalar=Fraction(1, 3), addendum=Offset(1, 8))
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), edge=right, scalar=Fraction(1, 3), addendum=Offset(1, 8))

    Pick out the timepoint equal to the left edge of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Note, index=10)

    ::

        >>> specificationtools.TemporalCursor(anchor=anchor)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10))

    Pick out the timepoint equal to the right edgright edge of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, edge=right)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10), edge=right)

    Examples below reference the temporal cursor defined immediately above::

        >>> temporal_cursor = _

    Temporal cursors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, scalar=None, addendum=None): 
        assert isinstance(anchor, (ScoreObjectIndicator, type(None))), repr(anchor)
        assert isinstance(edge, (VectorConstant, type(None))), repr(edge)
        assert isinstance(scalar, (fractions.Fraction, type(None))), repr(scalar)
        if addendum is not None:
            addendum = durationtools.Offset(addendum)
        assert isinstance(addendum, (durationtools.Offset, type(None))), repr(addendum)
        self._anchor = anchor
        self._scalar = scalar
        self._edge = edge
        self._addendum = addendum

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a temporal cursor with score object indicator,
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
        elif not self.offset == other.offset:
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
        '''Temporal cursor addendum specified by user.

            >>> temporal_cursor.addendum is None
            True

        Value of none is taken equal to ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._addendum

    @property
    def anchor(self):
        '''Temporal cursor anchor specified by user.
        
            >>> temporal_cursor.anchor
            ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10)

        Value of none is taken equal the entire score.

        Return score object indicator or none.
        '''
        return self._anchor

    @property
    def edge(self):
        '''Temporal cursor edge indicator specified by user.
        
            >>> temporal_cursor.edge
            right

        Value of none is taken equal to ``left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def scalar(self):
        '''Temporal cursor scalar specified by user.

            >>> temporal_cursor.scalar is None
            True

        Value of none is taken equal to ``Fraction(1)``.

        Return fraction or none.
        '''
        return self._scalar

    @property
    def score_offset(self):
        '''Rational-valued offset of temporal cursor in score.
    
        Return offset.

        .. note:: not yet implemented.
        '''
        raise NotImplementedError
