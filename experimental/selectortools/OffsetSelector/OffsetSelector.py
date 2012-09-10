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
    def segment_identifier(self):
        '''Delegate to ``self.selector.segment_identifier``.
        '''
        return self.selector.segment_identifier

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
    def start_offset_value(self):
        '''Offset selector start offset (numeric) value.

        Return offset.
        '''
        if self.start_offset is None:
            return durationtools.Offset(0)
        return self.start_offset

    @property
    def stop_offset(self):
        '''Offset selector stop offset.

        Return offset or none.
        '''
        return self._stop_offset

    @property
    def stop_offset_value(self):
        '''Offset selector stop offset (numeric) value.
        
        Return offset.
        '''
        if self.stop_offset is None:
            return durationtools.Offset(self.selector.duration)
        return self.stop_offset

    ### PUBLIC METHODS ##

    def get_duration(self, score_specification, context_name):
        r'''Evaluate duration of selector when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        return self.get_segment_stop_offset(score_specification, context_name) - \
            self.get_segment_start_offset(score_specification, context_name)

    def get_score_start_offset(self, score_specification, context_name):
        r'''Evaluate score start offset of selector when applied
        to `context_name` in `score_specification`.

        .. note:: not yet implemented.

        Return offset.
        '''
        raise NotImplementedError

    def get_score_stop_offset(self, score_specification, context_name):
        r'''Evaluate score stop offset of selector when applied
        to `context_name` in `score_specification`.

        .. note:: not yet implemented.

        Return offset.
        '''
        raise NotImplementedError

    def get_segment_start_offset(self, score_specification, context_name):
        r'''Evaluate segment start offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        if self.start_offset is None:
            return durationtools.Offset(0)
        elif self.start_offset < 0:
            return self.selector.get_duration(score_specification, context_name) + self.start_offset
        else:
            return self.start_offset

    def get_segment_stop_offset(self, score_specification, context_name):
        r'''Evaluate segment stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        if self.stop_offset is None:
            return durationtools.Offset(self.selector.get_duration(score_specification, context_name))
        elif self.stop_offset < 0:
            return self.selector.get_duration(score_specification, context_name) + self.stop_offset
        return self.stop_offset

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.selector.set_segment_identifier()``.
        '''
        return self.selector.set_segment_identifier(segment_identifier)
