from abjad.tools import durationtools
from experimental.selectortools.Selector import Selector


class OffsetSelector(Selector):
    r'''.. versionadded:: 1.0

    Offset selector. 
    '''

    ### INITIALIZER ##
    
    def __init__(self, selector, start_offset=None, stop_offset=None):
        assert isinstance(selector, Selector)
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        self._selector = selector
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def selector(self):
        '''Offset selector selector.

        Return selector.
        '''
        return self._selector

    @property
    def start_offset(self):
        '''Offset selector start offset.

        Return offset or none.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Offset selector stop offset.

        Return offset or none.
        '''
        return self._stop_offset
