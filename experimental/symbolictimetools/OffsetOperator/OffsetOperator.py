from abjad.tools import durationtools
from experimental.symbolictimetools.Selector import Selector


class OffsetOperator(Selector):
    r'''.. versionadded:: 1.0

    Offset symbolic timespan. 
    '''

    ### INITIALIZER ##
    
    def __init__(self, anchor, start_offset=None, stop_offset=None):
        assert isinstance(anchor, (Selector, str, type(None)))
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        self._anchor = anchor
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        '''Offset symbolic timespan anchor.

        Return anchor.
        '''
        return self._anchor

    @property
    def start_offset(self):
        '''Offset symbolic timespan start offset.

        Return offset or none.
        '''
        return self._start_offset

    @property
    def start_offset_value(self):
        '''Offset symbolic timespan start offset (numeric) value.

        Return offset.
        '''
        if self.start_offset is None:
            return durationtools.Offset(0)
        return self.start_offset

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.anchor.start_segment_identifier``.
        '''
        return self.anchor.start_segment_identifier

    @property
    def stop_offset(self):
        '''Offset symbolic timespan stop offset.

        Return offset or none.
        '''
        return self._stop_offset

    @property
    def stop_offset_value(self):
        '''Offset symbolic timespan stop offset (numeric) value.
        
        Return offset.
        '''
        if self.stop_offset is None:
            return durationtools.Offset(self.anchor.duration)
        return self.stop_offset

    ### PUBLIC METHODS ##

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Evaluate start and stop offsets of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return pair.
        '''
        if self.start_offset is None:
            start_offset = durationtools.Offset(0)
        elif self.start_offset < 0:
            if isinstance(self.anchor, str):
                start_offset = score_specification.segment_specifications[self.anchor].duration + self.start_offset
            else:
                start_offset = self.anchor.get_duration(score_specification, context_name) + self.start_offset
        else:
            start_offset = self.start_offset
        segment_specification = score_specification.get_start_segment_specification(self)
        segment_name = segment_specification.segment_name
        start_offset = score_specification.segment_offset_to_score_offset(segment_name, start_offset)
        if self.stop_offset is None:
            if isinstance(self.anchor, str):
                stop_offset = score_specification.segment_specifications[self.anchor].duration
            else:
                stop_offset = durationtools.Offset(self.anchor.get_duration(score_specification, context_name))
        elif self.stop_offset < 0:
            if isinstance(self.anchor, str):
                stop_offset = score_specification.segment_specifications[self.anchor].duration + self.stop_offset
            else:
                stop_offset = self.anchor.get_duration(score_specification, context_name) + self.stop_offset
        else:
            stop_offset = self.stop_offset
        stop_offset = score_specification.segment_offset_to_score_offset(segment_name, stop_offset)
        return start_offset, stop_offset

    def get_selected_objects(self, score_specification, context_name):
        '''Implemented only for interface compliance.
        '''
        raise NotImplementedError

    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.anchor.set_segment_identifier()``.
        '''
        if isinstance(self.anchor, str):
            self._anchor = segment_identifier
        else:
            return self.anchor.set_segment_identifier(segment_identifier)
