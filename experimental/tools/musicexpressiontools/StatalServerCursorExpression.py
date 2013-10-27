# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.PayloadExpression \
    import PayloadExpression


class StatalServerCursorExpression(PayloadExpression):
    r'''Statal server cursor expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from experimental.tools import musicexpressiontools
        assert isinstance(payload, musicexpressiontools.StatalServerCursor)
        PayloadExpression.__init__(self, payload)
