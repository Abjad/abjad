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
    '''

    ### INTIAILIZER ###

    def __init__(self, payload, request_modifications=None):
        from abjad.tools import rhythmmakertools
        Request.__init__(self, request_modifications=request_modifications)
        assert isinstance(payload, (tuple, list, str, rhythmmakertools.RhythmMaker)), repr(payload)
        self._payload = payload

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Payload of absolute request.
        '''
        return self._payload
