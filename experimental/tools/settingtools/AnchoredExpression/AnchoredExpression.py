from experimental.tools.settingtools.AnchoredObject import AnchoredObject
from experimental.tools.settingtools.Expression import Expression


class AnchoredExpression(Expression, AnchoredObject):
    '''Anchored expression.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None):
        Expression.__init__(self)
        AnchoredObject.__init__(self, anchor=anchor)

    ### SPECIAL METHODS ###

    # TODO: maybe move to AnchoredObject
    def __deepcopy__(self, memo):
        '''Expression deepcopy preserves score specification.
        '''
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result
