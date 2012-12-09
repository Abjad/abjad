import abc
from abjad.tools import mathtools
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class RatioOperator(SymbolicTimespan):
    r'''.. versionadded:: 1.0
    
    Abstract ratio-part operator from which concrete ratio-part operators inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, anchor, ratio, part):
        assert isinstance(anchor, SymbolicTimespan)
        assert isinstance(part, int)
        ratio = mathtools.Ratio(ratio)
        self._anchor = anchor
        self._ratio = ratio
        self._part = part

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Ratio-part symbolic timespan anchor.
        '''
        return self._anchor

    @property
    def part(self):
        '''Ratio-part symbolic timespan part.

        Return integer.
        '''
        return self._part

    @property
    def ratio(self):
        '''Ratio-part symbolic timespan ratio.

        Return ratio.
        '''
        return self._ratio

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.anchor.start_segment_identifier``.
        '''
        return self.anchor.start_segment_identifier

    ### PUBLIC METHODS ###

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.anchor.set_segment_identifier()``.
        '''
        self.anchor.set_segment_identifier(segment_identifier)
