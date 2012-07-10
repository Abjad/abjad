from experimental.specificationtools.RetrievalRequest import RetrievalRequest


# TODO: replace DivisionOldSelector with SingleContextDivisionSelector
class DivisionOldSelector(RetrievalRequest):
    r'''.. versionadded:: 1.0

    .. note:: deprecated. Use SingleContextDivisionSelector instead.

    The `voice` parameter specifies the voice whose divisions are to be copied.

    The `start_segment_name` parameter specifies which segment is to constitute the start 
    of the selection.

    The `segment_count` parameter specifies how many segments' worth of divisions are to copied.

    Intuitively a division retrieval request says "go fetch 1 or more consecutive segments' worth
    of divisions from such and such a voice."
    '''

    ### INITIALIZER ###

    def __init__(self, voice, start_segment_name, segment_count=1):
        assert isinstance(voice, str), repr(voice)
        assert isinstance(start_segment_name, str), repr(start_segment_name)
        assert isinstance(segment_count, int), repr(segment_count)
        self.voice = voice
        self.start_segment_name = start_segment_name
        self.segment_count = segment_count
