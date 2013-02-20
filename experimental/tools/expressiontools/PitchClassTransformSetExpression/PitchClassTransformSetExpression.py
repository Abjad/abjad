from experimental.tools.expressiontools.GeneralizedSetExpression import GeneralizedSetExpression


class PitchClassTransformSetExpression(GeneralizedSetExpression):
    '''Pitch-class transform set expression.
    '''

    ### INTIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None):
        GeneralizedSetExpression.__init__(self, attribute='pitch_class_transform',
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory)
