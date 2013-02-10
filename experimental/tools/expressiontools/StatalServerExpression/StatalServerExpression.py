from experimental.tools.expressiontools.Expression import Expression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class StatalServerExpression(Expression, PayloadCallbackMixin):
    r'''Statal server expression.

    The purpose of a statal server expression is to function as the source_expression of a set expression.
    '''

    ### INITIALIZER ###
    
    def __init__(self, statal_server=None, callbacks=None):
        assert isinstance(statal_server, expressiontools.StatalServer), repr(statal_server)
        Expression.__init__(self)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        self._statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.statal_server(self)

    ### PRIVATE METHODS ###

    def evaluate(self):
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def statal_server(self):
        return self._statal_server
