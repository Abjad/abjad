import abc
from abjad.tools import mathtools
from experimental.symbolictimetools.Selector import Selector


class RatioOperator(Selector):
    r'''.. versionadded:: 1.0
    
    Abstract ratio-part symbolic timespan class from which concrete ratio-part symbolic timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, anchor, ratio, part):
        assert isinstance(anchor, Selector)
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

    def get_selected_objects(self, score_specification, context_name):
        '''Get ratio parts when symbolic timespan is applied
        to `context_name` in `score_specification`.

        Return list.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.anchor.set_segment_identifier()``.
        '''
        self.anchor.set_segment_identifier(segment_identifier)
