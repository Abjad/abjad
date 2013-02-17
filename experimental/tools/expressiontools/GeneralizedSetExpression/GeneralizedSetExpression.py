from abjad.tools import timespantools
from experimental.tools.expressiontools.Expression import Expression


class GeneralizedSetExpression(Expression):
    '''Generalized set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute=None, source_expression=None, target_select_expression_inventory=None):
        from experimental.tools import expressiontools
        assert isinstance(attribute, str), repr(attribute)
        assert isinstance(source_expression, expressiontools.Expression), repr(source_expression)
        assert isinstance(target_select_expression_inventory, 
            expressiontools.SelectExpressionInventory), repr(target_select_expression_inventory)
        self._attribute = attribute
        self._source_expression = source_expression
        self._target_select_expression_inventory = target_select_expression_inventory
        self._lexical_rank = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Generalized set expression attribute.

        Return string.
        '''
        return self._attribute

    @property
    def source_expression(self):
        '''Generalized set expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def target_select_expression_inventory(self):
        '''Generalized set expression target select expression inventory.

        Return select expression inventory.
        '''
        return self._target_select_expression_inventory

    ### PUBLIC METHODS ###

    def evaluate(self):
        raise NotImplementedError('eventually remove me and implement on child classes.')
