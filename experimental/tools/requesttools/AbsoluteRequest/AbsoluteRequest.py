from experimental.tools.requesttools.Request import Request


class AbsoluteRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Absolute request::

        >>> request = requesttools.AbsoluteRequest([(4, 16), (2, 16)])

    ::

        >>> request
        AbsoluteRequest([(4, 16), (2, 16)])

    ::

        >>> z(request)
        requesttools.AbsoluteRequest(
            [(4, 16), (2, 16)]
            )

    Request `payload`.

    Later, apply any of `index`, `count`, `rotation` that are not none.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload, modifications=None, index=None, count=None, rotation=None):
        Request.__init__(self, modifications=modifications, index=index, count=count, rotation=rotation)
        self._payload = payload

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Payload of absolute request.
        '''
        return self._payload
