from experimental.tools.expressiontools.Expression import Expression


class PayloadExpression(Expression):
    r'''Payload expression.

        >>> payload_expression = expressiontools.PayloadExpression('foo')

    ::

        >>> z(payload_expression)
        expressiontools.PayloadExpression(
            'foo'
            )

    Payload expressions evaluate to themselves.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Payload expression payload:

        ::

            >>> payload_expression.payload
            'foo'

        Return arbitrary value.
        '''
        return self._payload

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate payload expression.

            >>> payload_expression.evaluate()
            PayloadExpression('foo')

        Return payload expression.
        '''
        return self
