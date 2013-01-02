import numbers
from experimental.tools.requesttools.Request import Request


class AbsoluteRequest(Request):
    r'''Absolute request.

    ::

        >>> from experimental.tools import *

    ::


        >>> request = requesttools.AbsoluteRequest([(4, 16), (2, 16)])

    ::

        >>> request
        AbsoluteRequest(((4, 16), (2, 16)))

    ::

        >>> z(request)
        requesttools.AbsoluteRequest(
            ((4, 16), (2, 16))
            )

    Create behind-the-scenes at setting-time.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload, request_modifiers=None):
        Request.__init__(self, request_modifiers=request_modifiers)
        assert isinstance(payload, (str, tuple, list)), repr(payload)
        if isinstance(payload, list):
            payload = tuple(payload)
        self._payload = payload

    ### PRIVATE METHODS ###

    def _evaluate_payload(self, score_specification, voice_name):
        if isinstance(self.payload, str):
            return self.payload
        elif isinstance(self.payload, tuple):
            result = []
            for element in self.payload:
                if hasattr(element, '_get_timespan'):
                    timespan = element._get_timespan(score_specification, voice_name)
                    result.append(timespan)
                else:
                    assert isinstance(element, (numbers.Number, str, tuple)), repr(element)
                    result.append(element)
            result = tuple(result)
            return result
        else:
            raise TypeError(self.payload)
            
    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Absolute request payload::

            >>> request.payload
            ((4, 16), (2, 16))

        Return tuple or string.
        '''
        return self._payload

    @property
    def request_modifiers(self):
        '''Absolute request modifiers::

            >>> request.request_modifiers
            ModifierInventory([])

        Return modifier inventory.
        '''
        return Request.request_modifiers.fget(self)

    @property
    def storage_format(self):
        '''Absolute request storage format::

            >>> print request.storage_format
            requesttools.AbsoluteRequest(
                ((4, 16), (2, 16))
                )

        Return string.
        '''
        return Request.storage_format.fget(self)

    ### PUBLIC METHODS ###

    # TODO: maybe make mandatory part of interface for all request classes.
    def get_payload(self, score_specification=None):
        return self.payload
