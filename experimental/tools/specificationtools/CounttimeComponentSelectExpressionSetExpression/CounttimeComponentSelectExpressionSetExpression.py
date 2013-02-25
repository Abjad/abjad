from experimental.tools.specificationtools.Expression import Expression


class CounttimeComponentSelectExpressionSetExpression(Expression):
    '''Counttime component select expression set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_counttime_component_select_expression=None):
        from experimental.tools import specificationtools
        assert isinstance(source_expression, specificationtools.Expression), repr(source_expression)
        assert isinstance(target_counttime_component_select_expression,
            specificationtools.CounttimeComponentSelectExpression), repr(
            target_counttime_component_select_expression)
        self._source_expression = source_expression
        self._target_counttime_component_select_expression = target_counttime_component_select_expression
        self._lexical_rank = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source_expression(self):
        '''Counttime component select expression set expression source expression.

        Return expression.
        '''
        return self._source_expression

    @property
    def target_counttime_component_select_expression(self):
        '''Counttime component select expression set expression
        target select expression inventory.

        Return counttime component select expression.
        '''
        return self._target_counttime_component_select_expression

    ### PUBLIC METHODS ###

    def evaluate(self):
        raise NotImplementedError('eventually remove me and implement on child classes.')
