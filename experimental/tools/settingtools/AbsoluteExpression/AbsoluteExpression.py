from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class AbsoluteExpression(Expression, PayloadCallbackMixin):
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

    Absolute expressions are assumed to evaluate to a list or other iterable.
    '''

    ### INTIAILIZER ###

    def __init__(self, payload, callbacks=None):
        assert isinstance(payload, (str, tuple, list)), repr(payload)
        Expression.__init__(self)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        if isinstance(payload, list):
            payload = tuple(payload)
        self._payload = payload

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification=None, voice_name=None):
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        if isinstance(self.payload, (str, tuple)):
            result = self.payload
        else:
            raise TypeError(self.payload)
        # TODO: eventually change to result = self._apply_callbacks(result)
        result, dummy = self._apply_callbacks(result, None)
        return result

    ### READ-ONLY PROPERTIES ###

    @property
    def callbacks(self):
        '''Absolute expression callbacks:

        ::

            >>> expression.callbacks
            CallbackInventory([])

        Return callback inventory.
        '''
        return PayloadCallbackMixin.callbacks.fget(self)

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
