from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
import fractions


class TemporalCursor(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    (Object-oriented delayed evaluation.)

    Temporal cursors are designed to pick out timepoints in a sophisticated way.

    Temporal cursors locate timepoints relative to arbitrary objects in score.

    Temporal cursors resolve to a rational-valued score offset.

    Temporal cursors afford the location of timepoints relative to score
    objects that do not yet exist.

    Initialize with different combinations of optional `anchor`, 
    `start`, `scalar` and `addendum`.

    Import ``specificationtools``::

        >>> from experimental import specificationtools

    Pick out the timepoint equal to start of score::

        >>> specificationtools.TemporalCursor()
        TemporalCursor()

    Pick out the timepoint equal to end of score::

        >>> specificationtools.TemporalCursor(start=False)
        TemporalCursor(start=False)

    Pick out the timepoint exactly ``1/8`` of a whole note into score::

        >>> specificationtools.TemporalCursor(addendum=Fraction(1, 8))
        TemporalCursor(addendum=Offset(1, 8))

    Pick out the timepoint exactly one third of the way into score::

        >>> specificationtools.TemporalCursor(scalar=Fraction(1, 3), start=False)
        TemporalCursor(scalar=Fraction(1, 3), start=False)

    Pick out the timepoint exactly ``1/8`` of a whole note after the first third of score::

        >>> specificationtools.TemporalCursor(scalar=Fraction(1, 3), start=False, addendum=Fraction(1, 8))
        TemporalCursor(scalar=Fraction(1, 3), start=False, addendum=Offset(1, 8))

    Pick out the timepoint equal to the start of the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red')

    ::

        >>> specificationtools.TemporalCursor(anchor=anchor)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'))

    Pick out the timepoint equal to the end of the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, start=False)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), start=False)

    Pick out the timepoint equal to ``1/8`` of a whole note after the start of 
    the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, addendum=Fraction(1, 8))
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), addendum=Offset(1, 8))

    Pick out the timepoint equal to exactly one third of the way into
    the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, scalar=Fraction(1, 3), start=False)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), scalar=Fraction(1, 3), start=False)

    Pick out the point equal to ``1/8`` of a whole note after the end of the first third of
    the segment with name ``'red'``::
    
        >>> specificationtools.TemporalCursor(anchor=anchor, scalar=Fraction(1, 3), start=False, addendum=Fraction(1, 8))
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red'), scalar=Fraction(1, 3), start=False, addendum=Offset(1, 8))

    Pick out the timepoint equal to the start of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Note, index=10)
        >>> specificationtools.TemporalCursor(anchor=anchor)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10))

    Pick out the timepoint equal to the end of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> specificationtools.TemporalCursor(anchor=anchor, start=False)
        TemporalCursor(anchor=ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10), start=False)

    Examples below reference the temporal curosr defined immediately above::

        >>> temporal_cursor = _

    Temporal cursors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, scalar=None, start=None, addendum=None): 
        assert isinstance(anchor, (ScoreObjectIndicator, type(None))), repr(anchor)
        assert isinstance(scalar, (fractions.Fraction, type(None))), repr(scalar)
        assert isinstance(start, (bool, type(None))), repr(start)
        if addendum is not None:
            addendum = durationtools.Offset(addendum)
        assert isinstance(addendum, (durationtools.Offset, type(None))), repr(addendum)
        self._anchor = anchor
        self._scalar = scalar
        self._start = start
        self._addendum = addendum

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a temporal cursor with score object indicator,
        start and offset all equal to those of `self`.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.anchor == other.anchor:
            return False
        elif not self.start == other.start:
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
            
        Return offset or none.
        '''
        return self._addendum

    @property
    def anchor(self):
        '''Anchor of temporal cursor specified by user.
        
            >>> temporal_cursor.anchor
            ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=10)

        Return score object indicator or none.
        '''
        return self._anchor

    @property
    def scalar(self):
        '''Temporal cursor scalar specified by user.

            >>> temporal_cursor.scalar is None
            True

        Return fraction or none.
        '''
        return self._scalar

    @property
    def score_offset(self):
        '''.. note:: not yet implemented.
        '''
        raise NotImplementedError

    @property
    def start(self):
        '''Temporal cursor start indicator specified by user.
        
            >>> temporal_cursor.start
            False

        Return boolean or none.
        '''
        return self._start
