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

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from abjad.tools import timespantools
        from experimental.tools import settingtools
        result = type(self)()
        for expression in self:
            expression = expression._evaluate()
            # TODO: eventually remove this branch
            if isinstance(expression, (list, tuple)):
                result.extend(expression)
            elif isinstance(expression, settingtools.PayloadExpression):
                result.extend(expression.payload)
            elif isinstance(expression, settingtools.Expression):
                result.append(expression)
            else:
                raise TypeError(expression)
        return result
