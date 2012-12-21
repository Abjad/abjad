from experimental.tools.symbolictimetools.VoiceSelector import VoiceSelector


class BeatSelector(VoiceSelector):
    '''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Beam selector.
    '''

    ### PRIVATE METHODS ###

    def _get_offset(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        Return offset pair.
        '''
        raise NotImplementedError('implement me')
