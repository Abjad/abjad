import abc
from experimental.tools.symbolictimetools.Selector import Selector


class VoiceSelector(Selector):
    r'''.. versionadded:: 1.0

    Selector from which selectors inherit when they need a voice name attribute.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, anchor=None, start_identifier=None, stop_identifier=None, voice_name=None,
        time_relation=None, 
        timespan_modifications=None, selector_modifications=None, modifications=None):
        Selector.__init__(self,
            anchor=anchor, start_identifier=start_identifier, stop_identifier=stop_identifier, 
            time_relation=time_relation, timespan_modifications=timespan_modifications, 
            selector_modifications=selector_modifications, modifications=modifications)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
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
