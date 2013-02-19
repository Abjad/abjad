from experimental.tools.expressiontools.GeneralizedSetExpression import GeneralizedSetExpression


class PitchSetExpression(GeneralizedSetExpression):
    '''Generalized pitch set expression.
    '''

    ### INTIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None):
        GeneralizedSetExpression.__init__(self, attribute='pitch',
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory)
