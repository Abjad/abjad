# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.Expression import Expression


class CounttimeComponentSelectExpressionSetExpression(Expression):
    r'''Counttime component select expression set expression.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        source_expression=None,
        target_counttime_component_select_expression=None,
        ):
        from experimental.tools import musicexpressiontools
        assert isinstance(source_expression,
            musicexpressiontools.Expression), repr(source_expression)
        assert isinstance(target_counttime_component_select_expression,
            musicexpressiontools.CounttimeComponentSelectExpression), repr(
            target_counttime_component_select_expression)
        self._source_expression = source_expression
        self._target_counttime_component_select_expression = \
            target_counttime_component_select_expression
        self._lexical_rank = None

    ### PUBLIC PROPERTIES ###

    @property
    def source_expression(self):
        r'''Counttime component select expression set expression
        source expression.

        Returns expression.
        '''
        return self._source_expression

    @property
    def target_counttime_component_select_expression(self):
        r'''Counttime component select expression set expression
        target select expression inventory.

        Returns counttime component select expression.
        '''
        return self._target_counttime_component_select_expression

    ### PUBLIC METHODS ###

    def evaluate(self):
        message = 'eventually remove me and implement on child classes.'
        raise NotImplementedError(message)