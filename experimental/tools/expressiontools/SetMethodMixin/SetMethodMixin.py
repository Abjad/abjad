import copy
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''Set method mixin.
    '''

    ### PRIVATE METHODS ###

    def _all_are_expressions(self, expr):
        from experimental.tools import expressiontools
        if isinstance(expr, (tuple, list)):
            if all([isinstance(x, expressiontools.Expression) for x in expr]):
                return True
        return False

    def _expr_to_expression(self, expr):
        from abjad.tools import rhythmmakertools
        from experimental.tools import handlertools
        from experimental.tools import expressiontools
        from experimental.tools import expressiontools
        if isinstance(expr, expressiontools.Expression):
            return expr
        elif self._all_are_expressions(expr):
            return expressiontools.ExpressionInventory(expr)
        elif isinstance(expr, (tuple, list)):
            return expressiontools.PayloadExpression(expr)
        elif isinstance(expr, (str)):
            component = iotools.p(expr)
            return expressiontools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return expressiontools.RhythmMakerPayloadExpression(expr)
        else:
            raise TypeError('do not know how to change {!r} to expression.'.format(expr))
