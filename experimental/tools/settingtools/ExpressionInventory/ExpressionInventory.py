import copy
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.settingtools.Expression import Expression


class ExpressionInventory(ObjectInventory, Expression):
    '''Expression inventory.

    Each expression will be evaluated in turn.
    '''
    
    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        tokens = [copy.deepcopy(x) for x in self]
        result = type(self)(tokens=tokens, name=self.name)
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def elements(self):
        result = []
        for expression in self:
            expression = expression.evaluate()
            result.extend(expression.elements)
        return result

    ### PRIVATE METHODS ###

    def evaluate(self):
        result = type(self)()
        for expression in self:
            expression = expression.evaluate()
            result.append(expression)
        return result
