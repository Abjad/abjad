from experimental.tools import handlertools
from experimental.tools.expressiontools.Expression import Expression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class HandlerExpression(Expression, PayloadCallbackMixin):
    r'''Handler expression.
    '''

    ### INITIALIZER ###

    def __init__(self, handler=None, callbacks=None):
        assert isinstance(handler, handlertools.Handler), repr(handler)
        Expression.__init__(self)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._handler = handler

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate handler expression.
        '''
        raise NotImplementedError

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        '''Handler expression handler.
        '''
        return self._handler
