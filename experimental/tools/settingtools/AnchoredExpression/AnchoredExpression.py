from experimental.tools.settingtools.ExpressionAnchoredObject import ExpressionAnchoredObject
from experimental.tools.settingtools.Expression import Expression


class AnchoredExpression(Expression, ExpressionAnchoredObject):
    '''Anchored expression.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None):
        Expression.__init__(self)
        ExpressionAnchoredObject.__init__(self, anchor=anchor)

    ### SPECIAL METHODS ###

    # TODO: maybe move to ExpressionAnchoredObject
    def __deepcopy__(self, memo):
        '''Expression deepcopy preserves score specification.
        '''
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result
