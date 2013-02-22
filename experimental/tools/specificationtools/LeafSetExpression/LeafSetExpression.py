from abjad.tools import timespantools
from experimental.tools.specificationtools.Expression import Expression


class LeafSetExpression(Expression):
    '''Leaf set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None):
        from experimental.tools import specificationtools
        assert isinstance(source_expression, specificationtools.Expression), repr(source_expression)
        assert isinstance(target_select_expression_inventory, 
            specificationtools.SelectExpressionInventory), repr(target_select_expression_inventory)
        self._source_expression = source_expression
        self._target_select_expression_inventory = target_select_expression_inventory
        self._lexical_rank = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source_expression(self):
        '''Leaf set expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def target_select_expression_inventory(self):
        '''Leaf set expression target select expression inventory.

        Return select expression inventory.
        '''
        return self._target_select_expression_inventory

    ### PUBLIC METHODS ###

    def evaluate(self):
        raise NotImplementedError('eventually remove me and implement on child classes.')
