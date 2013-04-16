from experimental.tools.musicexpressiontools.PayloadExpression import PayloadExpression


class StatalServerCursorExpression(PayloadExpression):
    '''Statal server cursor expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from experimental.tools import musicexpressiontools
        assert isinstance(payload, musicexpressiontools.StatalServerCursor), repr(payload)
        PayloadExpression.__init__(self, payload)
