from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Callback import Callback


class DivisionRetrievalRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, voice_name, start_segment_name, callback=None, count=None, n=1, offset=None):
        assert isinstance(voice_name, str), voice_name
        assert isinstance(start_segment_name, str), start_segment_name
        assert isinstance(callback, (Callback, type(None))), callback
        assert isinstance(count, (int, type(None))), count
        assert isinstance(n, int), n
        assert isinstance(offset, (int, type(None))), offset
        self.voice_name = voice_name
        self.start_segment_name = start_segment_name
        self.callback = callback
        self.count = count
        self.n = n
        self.offset = offset
