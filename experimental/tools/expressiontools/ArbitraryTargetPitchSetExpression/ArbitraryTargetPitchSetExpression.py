from experimental.tools.expressiontools.MultipleContextSetExpression import MultipleContextSetExpression


class ArbitraryTargetPitchSetExpression(MultipleContextSetExpression):
    '''Multiple-context pitch set expression.
    '''

    ### INTIALIZER ###

    def __init__(self, source_expression=None, target_expression=None):
        self._source_expression = source_expression
        self._target_expression = target_expression
