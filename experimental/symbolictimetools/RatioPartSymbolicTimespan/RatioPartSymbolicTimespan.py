import abc
from abjad.tools import mathtools
from experimental.symbolictimetools.TimespanSymbolicTimespan import TimespanSymbolicTimespan


class RatioPartSymbolicTimespan(TimespanSymbolicTimespan):
    r'''.. versionadded:: 1.0
    
    Abstract count-ratio selector class from which concrete count-ratio selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, selector, ratio, part):
        assert isinstance(selector, TimespanSymbolicTimespan)
        assert isinstance(part, int)
        ratio = mathtools.Ratio(ratio)
        self._selector = selector
        self._ratio = ratio
        self._part = part

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def part(self):
        '''Ratio-part selector part.

        Return integer.
        '''
        return self._part

    @property
    def ratio(self):
        '''Ratio-part selector ratio.

        Return ratio.
        '''
        return self._ratio

    @property
    def selector(self):
        '''Ratio-part selector selector.

        Return sliceable selector.
        '''
        return self._selector

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.selector.start_segment_identifier``.
        '''
        return self.selector.start_segment_identifier

    ### PUBLIC METHODS ###

    def get_selected_objects(self, score_specification, context_name):
        '''Get ratio parts when selector is applied
        to `context_name` in `score_specification`.

        Return list.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.selector.set_segment_identifier()``.
        '''
        self.selector.set_segment_identifier(segment_identifier)
