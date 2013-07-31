# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.Expression import Expression


class LeafSetExpression(Expression):
    r'''Leaf set expression.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        source_expression=None, 
        target_select_expression_inventory=None,
        ):
        from experimental.tools import musicexpressiontools
        assert isinstance(source_expression, musicexpressiontools.Expression)
        assert isinstance(target_select_expression_inventory,
            musicexpressiontools.SelectExpressionInventory)
        self._source_expression = source_expression
        self._target_select_expression_inventory = \
            target_select_expression_inventory
        self._lexical_rank = None

    ### PRIVATE METHODS ###

    def _iterate_selected_leaves_in_score(self, score):
        leaves = []
        for target_select_expression in \
            self.target_select_expression_inventory:
            iterable_payload_expression = \
                target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        return leaves

    ### PUBLIC PROPERTIES ###

    @property
    def source_expression(self):
        r'''Leaf set expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def target_select_expression_inventory(self):
        r'''Leaf set expression target select expression inventory.

        Return select expression inventory.
        '''
        return self._target_select_expression_inventory

    ### PUBLIC METHODS ###

    def evaluate(self):
        message = 'eventually remove me and implement on child classes.'
        raise NotImplementedError(message)
