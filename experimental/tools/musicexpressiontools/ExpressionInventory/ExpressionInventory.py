# -*- encoding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList
from experimental.tools.musicexpressiontools.IterablePayloadExpression \
    import IterablePayloadExpression


class ExpressionInventory(TypedList, IterablePayloadExpression):
    r'''Expression inventory.
    '''

    ### SPECIAL METHODS ###

    # TODO: remove?
    def __deepcopy__(self, memo):
        tokens = [copy.deepcopy(x) for x in self]
        result = type(self)(tokens=tokens, name=self.name)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def elements(self):
        r'''Expression inventory elements.
        '''
        result = []
        for expression in self:
            expression = expression.evaluate()
            result.extend(expression.elements)
        return result

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate expression inventory.

        Return newly constructed expression inventory.
        '''
        result = type(self)()
        for expression in self:
            expression = expression.evaluate()
            result.append(expression)
        return result
