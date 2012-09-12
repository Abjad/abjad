from experimental import handlertools
from experimental.requesttools.Request import Request


class HandlerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Request `handler`.

    Apply any of `index`, `count`, `reverse`, `rotation`, `callback` that are not none.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler, index=None, count=None, reverse=None, rotation=None, callback=None):
        assert isinstance(handler, handlertools.Handler)
        Request.__init__(self, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        self._handler = handler

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
