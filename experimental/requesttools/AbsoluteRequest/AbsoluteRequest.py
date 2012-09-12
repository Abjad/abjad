from experimental.requesttools.Request import Request


class AbsoluteRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Absolute request::

        >>> request = requesttools.AbsoluteRequest([(4, 16), (2, 16)], reverse=True)

    ::

        >>> request
        AbsoluteRequest([(4, 16), (2, 16)], reverse=True)

    ::

        >>> z(request)
        requesttools.AbsoluteRequest(
            [(4, 16), (2, 16)],
            reverse=True
            )

    Request `payload`.

    Later, apply any of `index`, `count`, `reverse`, `rotation`, `callback`
    that are not none.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload, index=None, count=None, reverse=None, rotation=None, callback=None):
        Request.__init__(self, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        self._payload = payload

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Payload of absolute request.
        '''
        return self._payload
