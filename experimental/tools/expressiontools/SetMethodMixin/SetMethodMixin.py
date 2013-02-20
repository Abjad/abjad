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

    def _attribute_to_set_expression_class(self, attribute):
        from experimental.tools import expressiontools
        return {
            'pitch': expressiontools.PitchSetExpression,
            'pitch_class_transform': expressiontools.PitchClassTransformSetExpression,
            }[attribute]

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
            return expressiontools.IterablePayloadExpression(expr)
        elif isinstance(expr, (str)):
            component = iotools.p(expr)
            return expressiontools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return expressiontools.RhythmMakerExpression(expr)
        elif isinstance(expr, expressiontools.StatalServerCursor):
            return expressiontools.StatalServerCursorExpression(expr)
        else:
            raise TypeError('do not know how to change {!r} to expression.'.format(expr))

    def _store_generalized_set_expression(self, attribute, source_expression):
        from experimental.tools import expressiontools
        set_expression_class = self._attribute_to_set_expression_class(attribute)
        source_expression = self._expr_to_expression(source_expression)
        if isinstance(self, expressiontools.SelectExpression):
            target_select_expression_inventory = expressiontools.SelectExpressionInventory([self])
        elif isinstance(self, expressiontools.SelectExpressionInventory):
            target_select_expression_inventory = self
        else:
            raise TypeError(self)
        generalized_set_expression = set_expression_class(
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory
            )
        assert self.score_specification is not None
        generalized_set_expression._score_specification = self.score_specification
        generalized_set_expression._lexical_rank = self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        if isinstance(generalized_set_expression, expressiontools.PitchSetExpression):
            self.score_specification.pitch_set_expressions.append(generalized_set_expression)
        else:
            self.score_specification.generalized_set_expressions.append(generalized_set_expression)
        return generalized_set_expression

    ### PUBLIC METHODS ###

    def set_pitch_class_transform(self, source_expression):
        r'''Set pitch class transform to `source_expression`.

        Return some sort of set expression.
        '''
        attribute = 'pitch_class_transform'
        return self._store_generalized_set_expression(attribute, source_expression)

    def set_pitches(self, source_expression):
        r'''Set pitches to `source_expression`.

        Return pitch set expression.
        '''
        attribute = 'pitch'
        return self._store_generalized_set_expression(attribute, source_expression)
