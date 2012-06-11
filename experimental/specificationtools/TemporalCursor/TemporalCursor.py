from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
import fractions


class TemporalCursor(AbjadObject):
    r'''.. versionadded:: 1.0

    An infinitely thin vertical line coincident with exactly one timepoint in score.

    Temporal cursors are designed to model sophisticated timepoint location
    made relative to an arbitrary object.

    Every temporal cursor resolves to a rational-valued score offset.

    A temporal cursor is defined equal to a collection of the following three things::

        * score object indicator
        * boolean start indicator
        * rational start offset

    All three values are optional.

    A score object indicator is defined equal to a collection of the following four things::

        * score segment
        * component class
        * component predicate
        * integer index

    All four values are optional.

    Score object indicators should be modeled by a dedicated class.
    So that will happen next before returning to the implementation here.
    '''

    ### INITIALIZER ###

    def __init__(self, score_object_indicator=None, start_indicator=None, start_offset=None): 
        assert isinstance(score_object_indicator, (ScoreObjectIndicator, type(None))), repr(score_object_indicator)
        assert isinstance(start_indicator, (bool, type(None))), repr(start_indicator)
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        self._score_object_indicator = score_object_indicator
        self._start_indicator = start_indicator
        self._start_offset = start_offset

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a temporal cursor with score object indicator,
        start and offset all equal to those of `self`.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.score_object_indicator == other.score_object_indicator:
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
    def score_object_indicator(self):
        '''Score object indicator.
        '''
        return self._score_object_indicator

    @property
    def score_offset(self):
        '''.. note:: not yet implemented.
        '''
        raise NotImplementedError

    @property
    def start_indicator(self):
        '''Start indicator.
        
        Return boolean or none.
        '''
        return self._start_indicator

    @property
    def start_offset(self):
        '''Score object offset.

        Return offset or none.
        '''
        return self._start_offset
