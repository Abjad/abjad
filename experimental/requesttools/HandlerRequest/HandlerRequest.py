from experimental.requesttools.Request import Request


class HandlerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import requesttools

    Request `handler`.
    Apply any of `callback`, `count`, `offset` that are not none.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler, callback=None, count=None, offset=None):
        from experimental import handlertools
        assert isinstance(handler, handlertools.Handler)
        Request.__init__(self, callback=callback, count=count, offset=offset)
        self.handler = handler
