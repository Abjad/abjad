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
        result = self._apply_callbacks(result)
        return result
        # TODO: use these three lines instead of the code above
        #assert isinstance(self.payload, (str, tuple))
        #result = self._apply_callbacks(self)
        #return result

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

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result

    def reflect(self):
        '''Reflect.

        Return newly constructed absolute expression.
        '''
        # TODO: eventually allow only tuple or list
        #assert isinstance(self.payload, (tuple, list)), repr(self.payload)
        if isinstance(self.payload, (tuple, list)):
            payload = type(self.payload)(reversed(self.payload))
            result = self.new(payload=payload)
            return result
        # TODO: This is probably the source of the "can't look up parseable string rhythm setting" bug.
        #       Means that parseable strings shouldn't be passed around as AbsoluteExpression objects.
        elif isinstance(self.payload, str):
            return self
        else:
            raise TypeError(self.payload)
