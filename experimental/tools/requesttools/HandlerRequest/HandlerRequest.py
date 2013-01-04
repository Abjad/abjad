from experimental.tools import handlertools
from experimental.tools.requesttools.Request import Request


class HandlerRequest(Request):
    r'''Handler request.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler, payload_modifiers=None):
        assert isinstance(handler, handlertools.Handler)
        Request.__init__(self, payload_modifiers=payload_modifiers)
        self._handler = handler

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification=None, voice_name=None):
        raise NotImplementedError

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
