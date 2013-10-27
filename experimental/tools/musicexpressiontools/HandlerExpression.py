# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from experimental.tools.musicexpressiontools.Expression import Expression
from experimental.tools.musicexpressiontools.IterablePayloadCallbackMixin \
    import IterablePayloadCallbackMixin


class HandlerExpression(Expression, IterablePayloadCallbackMixin):
    r'''Handler expression.
    '''

    ### INITIALIZER ###

    def __init__(self, handler=None, callbacks=None):
        assert isinstance(handler, handlertools.Handler), repr(handler)
        Expression.__init__(self)
        IterablePayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._handler = handler

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate handler expression.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def handler(self):
        r'''Handler expression handler.
        '''
        return self._handler
