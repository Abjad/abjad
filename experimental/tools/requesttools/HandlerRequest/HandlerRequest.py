from experimental.tools import handlertools
from experimental.tools.requesttools.Request import Request


class HandlerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Request `handler`.

    Apply any of `index`, `count`, `rotation` that are not none.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler, modifications=None, index=None, count=None, rotation=None):
        assert isinstance(handler, handlertools.Handler)
        Request.__init__(self, modifications=modifications, 
            index=index, count=count, rotation=rotation)
        self._handler = handler

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
