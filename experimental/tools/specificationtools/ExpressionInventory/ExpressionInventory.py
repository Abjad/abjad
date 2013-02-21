import copy
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.specificationtools.IterablePayloadExpression import IterablePayloadExpression


class ExpressionInventory(ObjectInventory, IterablePayloadExpression):
    '''Expression inventory.
    '''
    
    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        tokens = [copy.deepcopy(x) for x in self]
        result = type(self)(tokens=tokens, name=self.name)
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def elements(self):
        '''Expression inventory elements.
        '''
        result = []
        for expression in self:
            expression = expression.evaluate()
            result.extend(expression.elements)
        return result

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate expression inventory.

        Return newly constructed expression inventory.
        '''
        result = type(self)()
        for expression in self:
            expression = expression.evaluate()
            result.append(expression)
        return result
