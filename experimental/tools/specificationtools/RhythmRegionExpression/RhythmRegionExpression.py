from experimental.tools.specificationtools.RegionExpression import RegionExpression


class RhythmRegionExpression(RegionExpression):
    '''Rhythm region expression.
    '''
    
    ### PUBLIC METHODS ###
    
    def prolongs_expr(self, expr):
        '''True when `expr` is a rhythm region expression
        and `expr` source_expression equals rhythm region expression source_expression.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.source_expression == expr.source_expression:
                return True
        return False
