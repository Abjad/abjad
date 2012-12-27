import abc
from experimental.tools.symbolictimetools.Selector import Selector


class VoiceSelector(Selector):
    r'''.. versionadded:: 1.0

    Selector from which selectors inherit when they need a voice name attribute.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, anchor=None, voice_name=None,
        time_relation=None, request_modifiers=None, timespan_modifiers=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert voice_name is not None
        Selector.__init__(self,
            anchor=anchor, 
            time_relation=time_relation, 
            request_modifiers=request_modifiers,
            timespan_modifiers=timespan_modifiers
            )
        self._voice_name = voice_name

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def voice_name(self):
        '''Slice selector voice name.

        If voice name is set then slice selector is "anchored" to a particular voice.

        If voice name is none then then slice selector is effectively "free floating"
        and is not anchored to a particular voice.

        Some documentation somewhere will eventually have to explain what it means
        for a selector to be "anchored" or "free floating".

        Return string or none.
        '''
        return self._voice_name
