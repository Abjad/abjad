from experimental.specificationtools.Callback import Callback
from experimental.specificationtools.RetrievalRequest import RetrievalRequest


# TODO: replace DivisionOldSelector with SingleContextDivisionSelector
class DivisionOldSelector(RetrievalRequest):
    r'''.. versionadded:: 1.0

    "Preserved" request for the system to go fetch divisions from somewhere during interpretation.

    Usually created when API function is called.
    
    The `voice_name` parameter specifies the voice whose divisions are to be copied.

    The `start_segment_name` parameter specifies which segment is to constitute the start 
    of the selection.

    The `segment_count` parameter specifies how many segments' worth of divisions are to copied.

    Intuitively a division retrieval request says "go fetch 1 or more consecutive segments' worth
    of divisions from such and such a voice."

    The `callback` parameter is currently only a stub. Parameter will be implemented
    to allow arbitrary postprocessing of the divisions specified by the other input parameters.

    The `offset` parameter is currently only a stub. Parameter will be implemented 
    to trim a nonnegative integer number of divisions from the start of the return list.
    For example, consider a division retrieval request that would result in 10 divisions.
    ContextSetting `offset=2` would cause only the final 8 divisions to return instead.
    
    The `count` parameter is currently only a stub. Parameter will be implemented
    to limit the total number of divisions returned. At that time we will have to
    determine how the `segment_count` and (division) `count` parameters are to interact.
    It is not yet clear what should happen when both are set.

    Future design consideration: should implement a boolean 'wrap' keyword. Parameter will
    control whether segments are to be read cyclically past the end of score specification.

    Future design consideration: if there are to be multiple retrieval requests in the system,
    then maybe all should inherit from an abstract RetrievalRequest class.
    '''

    ### INITIALIZER ###

    def __init__(self, start_segment_name, voice_name, callback=None, count=None, offset=None, segment_count=1):
        assert isinstance(voice_name, str), repr(voice_name)
        assert isinstance(start_segment_name, str), repr(start_segment_name)
        assert isinstance(callback, (Callback, type(None))), repr(callback)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(offset, (int, type(None))), repr(offset)
        assert isinstance(segment_count, int), repr(segment_count)
        self.voice_name = voice_name
        self.start_segment_name = start_segment_name
        self.callback = callback
        self.count = count
        self.offset = offset
        self.segment_count = segment_count
