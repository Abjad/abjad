from experimental.tools import handlertools
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class HandlerRequest(PayloadCallbackMixin):
    r'''Handler request.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler=None, payload_callbacks=None):
        assert isinstance(handler, handlertools.Handler)
        PayloadCallbackMixin.__init__(self, payload_callbacks=payload_callbacks)
        self._handler = handler

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification=None, voice_name=None):
        raise NotImplementedError

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
