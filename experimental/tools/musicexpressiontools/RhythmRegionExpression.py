# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.RegionExpression \
    import RegionExpression


class RhythmRegionExpression(RegionExpression):
    r'''Rhythm region expression.
    '''

    ### PUBLIC METHODS ###

    def prolongs_expr(self, expr):
        r'''Is true when `expr` is a rhythm region expression
        and `expr` source_expression equals rhythm region 
        expression source_expression.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_expression == expr.source_expression:
                return True
        return False
