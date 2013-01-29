from experimental.tools.expressiontools.RegionExpression import RegionExpression


class RhythmRegionExpression(RegionExpression):
    '''Rhythm region expression.
    '''
    
    ### PUBLIC METHODS ###
    
    def prolongs_expr(self, expr):
        if isinstance(expr, type(self)):
            if self.source == expr.source:
                return True
        return False
