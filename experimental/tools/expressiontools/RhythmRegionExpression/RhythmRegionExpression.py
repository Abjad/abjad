from experimental.tools.expressiontools.RegionExpression import RegionExpression


class RhythmRegionExpression(RegionExpression):
    '''Rhythm region expression.
    '''
    
    ### PUBLIC METHODS ###
    
    def prolongs_expr(self, expr):
        '''True when `expr` is a rhythm region expression
        and `expr` source equals rhythm region expression source.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source == expr.source:
                return True
        return False
