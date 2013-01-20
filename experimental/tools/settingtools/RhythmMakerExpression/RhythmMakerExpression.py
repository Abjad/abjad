from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class RhythmMakerExpression(Expression, PayloadCallbackMixin):
    r'''Rhythm-maker expression.

    Create behind-the-scenes at setting-time.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload=None, callbacks=None):
        assert isinstance(payload, rhythmmakertools.RhythmMaker), repr(payload)
        Expression.__init__(self)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
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
