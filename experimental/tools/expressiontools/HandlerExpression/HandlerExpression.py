from experimental.tools import handlertools
from experimental.tools.expressiontools.Expression import Expression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class HandlerExpression(Expression, PayloadCallbackMixin):
    r'''Handler request.

    The purpose of a handler request is to function as the source of a setting.
    '''

    ### INITIALIZER ###

    def __init__(self, handler=None, callbacks=None):
        assert isinstance(handler, handlertools.Handler), repr(handler)
        Expression.__init__(self)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._handler = handler

    ### PRIVATE METHODS ###

    def evaluate(self):
        raise NotImplementedError

    ### READ-ONLY PROPERTIES ###

    @property
    def handler(self):
        return self._handler
