from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class RhythmMakerRequest(PayloadCallbackMixin):
    r'''Rhythm-maker request.

    Create behind-the-scenes at setting-time.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None, payload_callbacks=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        PayloadCallbackMixin.__init__(self, payload_callbacks=payload_callbacks)
        self._payload = payload

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification=None, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload
