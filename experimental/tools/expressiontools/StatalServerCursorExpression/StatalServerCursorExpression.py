from experimental.tools.expressiontools.PayloadExpression import PayloadExpression


class StatalServerCursorExpression(PayloadExpression):
    '''Statal server cursor expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from experimental.tools import expressiontools
        assert isinstance(payload, expressiontools.StatalServerCursor), repr(payload)
        PayloadExpression.__init__(self, payload)
