from experimental.tools.specificationtools.PayloadExpression import PayloadExpression


class StatalServerCursorExpression(PayloadExpression):
    '''Statal server cursor expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from experimental.tools import specificationtools
        assert isinstance(payload, specificationtools.StatalServerCursor), repr(payload)
        PayloadExpression.__init__(self, payload)
