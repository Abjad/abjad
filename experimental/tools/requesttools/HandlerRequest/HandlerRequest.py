from experimental.tools import handlertools
from experimental.tools.requesttools.Request import Request


class HandlerRequest(Request):
    r'''

    ::

        >>> from experimental.tools import *

    Request `handler`.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler, request_modifiers=None):
        assert isinstance(handler, handlertools.Handler)
        Request.__init__(self, request_modifiers=request_modifiers)
        self._handler = handler

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
