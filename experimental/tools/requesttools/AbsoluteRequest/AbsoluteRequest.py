import numbers
from experimental.tools.requesttools.PayloadCallbackMixin import PayloadCallbackMixin


class AbsoluteRequest(PayloadCallbackMixin):
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

    def __init__(self, payload, payload_callbacks=None):
        PayloadCallbackMixin.__init__(self, payload_callbacks=payload_callbacks)
        assert isinstance(payload, (str, tuple, list)), repr(payload)
        if isinstance(payload, list):
            payload = tuple(payload)
        self._payload = payload

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification=None, voice_name=None):
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
    def payload_callbacks(self):
        '''Absolute request callbacks::

            >>> request.payload_callbacks
            CallbackInventory([])

        Return callback inventory.
        '''
        return PayloadCallbackMixin.payload_callbacks.fget(self)

    @property
    def storage_format(self):
        '''Absolute request storage format::

            >>> print request.storage_format
            requesttools.AbsoluteRequest(
                ((4, 16), (2, 16))
                )

        Return string.
        '''
        return PayloadCallbackMixin.storage_format.fget(self)
