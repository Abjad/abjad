from experimental.tools.expressiontools.ExpressionInventory import ExpressionInventory
from experimental.tools.expressiontools.SetMethodMixin import SetMethodMixin


class SelectExpressionInventory(ExpressionInventory, SetMethodMixin):
    '''Select expression inventory.
    '''

    ### PRIVATE METHODS ###

    def _store_generalized_set_expression(self, attribute, source_expression):
        from experimental.tools import expressiontools
        source_expression = self._expr_to_expression(source_expression)
        assert self.score_specification is not None
        generalized_set_expression = expressiontools.GeneralizedSetExpression(
            attribute=attribute,
            source_expression=source_expression,
            target_select_expression_inventory=self
            )
        generalized_set_expression._score_specification = self.score_specification
        generalized_set_expression._lexical_rank = self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        # TODO: where should generalized_set_expressions inventory be stored? maybe just score specification?
        #self.score_specification.generalized_set_expressions.append(generalized_set_expression)
        return generalized_set_expression
