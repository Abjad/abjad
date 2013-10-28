# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.PayloadExpression \
    import PayloadExpression


class StatalServerCursorExpression(PayloadExpression):
    r'''Statal server cursor expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload):
        from abjad.tools import datastructuretools
        assert isinstance(payload, datastructuretools.StatalServerCursor)
        PayloadExpression.__init__(self, payload)
