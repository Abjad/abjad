from abjad.tools import durationtools
from abjad.tools import timerelationtools
from experimental.tools.requesttools.Request import Request


class MaterialRequest(Request):
    r'''.. versionadded:: 1.0

    .. note:: deprecated. Use selector classes instead.

    The purpose of a material request is to function as the source of a setting.
    '''
    
    ### INITIALIZER ###

    def __init__(self, attribute, voice_name, anchor, modifications=None, time_relation=None):
        from experimental.tools import symbolictimetools
        assert isinstance(attribute, str), repr(attribute)
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        Request.__init__(self, modifications=modifications)
        self._attribute = attribute
        self._voice_name = voice_name
        self._anchor = anchor
        self._time_relation = time_relation

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return self._anchor

    @property
    def attribute(self):
        return self._attribute

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.anchor.start_segment_identifier``.
        '''
        if isinstance(self.anchor, str):
                return self.anchor
        else:
            return self.anchor.start_segment_identifier

    @property
    def time_relation(self):
        return self._time_relation

    @property
    def voice_name(self):
        return self._voice_name
