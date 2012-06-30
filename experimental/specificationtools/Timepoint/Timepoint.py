from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.ScoreElementSelector import ScoreElementSelector
import fractions


class Timepoint(AbjadObject):
    r'''.. versionadded:: 1.0

    Infinitely thin vertical line coincident with an arbitrary object-relative timepoint in score.

    (Object-oriented delayed evaluation.)

    Timepoints locate relative to arbitrary objects in score.

    Timepoints afford location relative to score objects that do not yet exist.

    Timepoints resolve to a rational-valued score offset.

    Initialize with different combinations of optional `anchor`, 
    `edge`, `multiplier` and `addendum`.

    Pick out the timepoint equal to the left edge of score::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.Timepoint()
        Timepoint()

    Pick out the timepoint equal to the right edge of score::

        >>> specificationtools.Timepoint(edge=Right)
        Timepoint(edge=Right)

    Pick out the timepoint ``1/8`` of a whole note into score::

        >>> from abjad.tools.durationtools.Offset import Offset

    ::

        >>> specificationtools.Timepoint(addendum=Offset(1, 8))
        Timepoint(addendum=Offset(1, 8))

    Pick out the timepoint one third of the way into score::

        >>> specificationtools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
        Timepoint(edge=Right, multiplier=Fraction(1, 3))

    Pick out the timepoint ``1/8`` of a whole note after the first third of score::

        >>> specificationtools.Timepoint(edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))
        Timepoint(edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    Pick out the timepoint equal to the left edge of the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreElementSelector(segment='red')

    ::

        >>> specificationtools.Timepoint(anchor=anchor)
        Timepoint(anchor=ScoreElementSelector(segment='red'))

    Pick out the timepoint equal to the right edge of the segment with name ``'red'``::

        >>> specificationtools.Timepoint(anchor=anchor, edge=Right)
        Timepoint(anchor=ScoreElementSelector(segment='red'), edge=Right)

    Pick out the timepoint equal to ``1/8`` of a whole note after the left edge of 
    the segment with name ``'red'``::

        >>> specificationtools.Timepoint(anchor=anchor, addendum=Offset(1, 8))
        Timepoint(anchor=ScoreElementSelector(segment='red'), addendum=Offset(1, 8))

    Pick out the timepoint equal to one third of the way into the segment with name ``'red'``::

        >>> specificationtools.Timepoint(anchor=anchor, edge=Right, multiplier=Fraction(1, 3))
        Timepoint(anchor=ScoreElementSelector(segment='red'), edge=Right, multiplier=Fraction(1, 3))

    Pick out the timepoint equal to ``1/8`` of a whole note after the right edge of the first third of
    the segment with name ``'red'``::
    
        >>> specificationtools.Timepoint(anchor=anchor, edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))
        Timepoint(anchor=ScoreElementSelector(segment='red'), edge=Right, multiplier=Fraction(1, 3), addendum=Offset(1, 8))

    Pick out the timepoint equal to the left edge of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> anchor = specificationtools.ScoreElementSelector(segment='red', context='Voice 1', klass=Note, index=10)

    ::

        >>> specificationtools.Timepoint(anchor=anchor)
        Timepoint(anchor=ScoreElementSelector(segment='red', context='Voice 1', klass=notetools.Note, index=10))

    Pick out the timepoint equal to the right edgright edge of note ``10`` in context ``'Voice 1'`` of
    the segment with name ``'red'``::

        >>> specificationtools.Timepoint(anchor=anchor, edge=Right)
        Timepoint(anchor=ScoreElementSelector(segment='red', context='Voice 1', klass=notetools.Note, index=10), edge=Right)

    Examples below reference the timepoint defined immediately above::

        >>> timepoint = _

    Timepoints are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, multiplier=None, addendum=None): 
        assert isinstance(anchor, (ScoreElementSelector, type(None))), repr(anchor)
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        values = []
        if self.anchor is None:
            values.append('SCORE')
        else:
            values.append(self.anchor._one_line_format)
        if self.edge is not None:
            values.append(repr(self.edge))
        if self.multiplier is not None:
            values.append(repr(self.multiplier))
        if self.addendum is not None:
            values.append(repr(self.addendum))
        values = ' '.join(values)
        values = '({})'.format(values)
        return values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addendum(self):
        '''Timepoint addendum specified by user.

            >>> timepoint.addendum is None
            True

        Value of none is taken equal to ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._addendum

    @property
    def anchor(self):
        '''Timepoint anchor specified by user.
        
            >>> timepoint.anchor
            ScoreElementSelector(segment='red', context='Voice 1', klass=notetools.Note, index=10)

        Value of none is taken equal the entire score.

        Return score object indicator or none.
        '''
        return self._anchor

    @property
    def edge(self):
        '''Timepoint edge indicator specified by user.
        
            >>> timepoint.edge
            Right

        Value of none is taken equal to ``left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def multiplier(self):
        '''Timepoint multiplier specified by user.

            >>> timepoint.multiplier is None
            True

        Value of none is taken equal to ``Fraction(1)``.

        Return fraction or none.
        '''
        return self._multiplier

    @property
    def score_offset(self):
        '''Rational-valued offset of timepoint in score.

        Derived from input values.
    
        Return offset.

        .. note:: not yet implemented.
        '''
        raise NotImplementedError
