# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.Expression import Expression


class PayloadExpression(Expression):
    r'''Payload expression.

        >>> payload_expression = musicexpressiontools.PayloadExpression('foo')

    ::

        >>> z(payload_expression)
        musicexpressiontools.PayloadExpression(
            'foo'
            )

    Payload expressions evaluate to themselves.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = payload

    ### PUBLIC PROPERTIES ###

    @property
    def payload(self):
        r'''Payload expression payload:

        ::

            >>> payload_expression.payload
            'foo'

        Return arbitrary value.
        '''
        return self._payload

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate payload expression.

            >>> payload_expression.evaluate()
            PayloadExpression('foo')

        Return payload expression.
        '''
        return self
