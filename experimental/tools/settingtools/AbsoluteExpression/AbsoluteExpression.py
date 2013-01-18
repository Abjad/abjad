import numbers
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class AbsoluteExpression(PayloadCallbackMixin):
    r'''Absolute expression.

    ::

        >>> expression = settingtools.AbsoluteExpression([(4, 16), (2, 16)])

    ::

        >>> expression
        AbsoluteExpression(((4, 16), (2, 16)))

    ::

        >>> z(expression)
        settingtools.AbsoluteExpression(
            ((4, 16), (2, 16))
            )

    Expression is assumed to resolve to a list or other iterable.

    Because of this absolute expressions afford payload callbacks.
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
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        if isinstance(self.payload, str):
            result = self.payload
        elif isinstance(self.payload, tuple):
            result = []
            for element in self.payload:
                # TODO: this is not the correct use of an AbsoluteExpression.
                #       Absolute expressions should contain only constants.
                #       Absolute expression should not contain other expressions.
                #       Create some other class to model a list of TimespanExpression objects.
                if isinstance(element, settingtools.TimespanExpression):
                    raise Exception(self)
                    timespan = element._get_timespan(score_specification, voice_name)
                    result.append(timespan)
                else:
                    assert isinstance(element, (numbers.Number, str, tuple)), repr(element)
                    result.append(element)
            result = tuple(result)
        else:
            raise TypeError(self.payload)
        result, dummy = self._apply_payload_callbacks(result, None)
        return result

    ### READ-ONLY PROPERTIES ###

    @property
    def payload(self):
        '''Absolute expression payload:

        ::

            >>> expression.payload
            ((4, 16), (2, 16))

        Return tuple or string.
        '''
        return self._payload

    @property
    def payload_callbacks(self):
        '''Absolute expression callbacks:

        ::

            >>> expression.payload_callbacks
            CallbackInventory([])

        Return callback inventory.
        '''
        return PayloadCallbackMixin.payload_callbacks.fget(self)

    @property
    def storage_format(self):
        '''Absolute expression storage format:

        ::

            >>> z(expression)
            settingtools.AbsoluteExpression(
                ((4, 16), (2, 16))
                )

        Return string.
        '''
        return PayloadCallbackMixin.storage_format.fget(self)
