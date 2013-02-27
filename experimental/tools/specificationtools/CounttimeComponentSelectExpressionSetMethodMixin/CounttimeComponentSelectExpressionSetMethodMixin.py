from abjad.tools import spannertools
from abjad.tools.abctools import AbjadObject


class CounttimeComponentSelectExpressionSetMethodMixin(AbjadObject):
    '''Counttime component set method mixin.
    '''

    ### PRIVATE METHODS ###

    def _store_counttime_component_select_expression_set_expression(self, attribute, source_expression):
        from experimental.tools import specificationtools
        set_expression_class = self._attribute_to_set_expression_class(attribute)
        source_expression = self._expr_to_expression(source_expression)
        counttime_component_select_expression_set_expression = set_expression_class(
            source_expression=source_expression,
            target_counttime_component_select_expression=self
            )
        assert self.score_specification is not None
        counttime_component_select_expression_set_expression._score_specification = self.score_specification
        counttime_component_select_expression_set_expression._lexical_rank = \
            self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        self.score_specification.postrhythm_set_expressions.append(
            counttime_component_select_expression_set_expression)
        return counttime_component_select_expression_set_expression

    ### PUBLIC METHODS ###

    def set_dynamic_handler(self, source_expression):
        r'''Set dynamic handler to `source_expression`.

        Return dynamic set expression.
        '''
        from experimental.tools import handlertools
        from experimental.tools import specificationtools
        assert isinstance(source_expression, handlertools.dynamics.DynamicHandler), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        attribute = 'dynamic_handler'
        return self._store_counttime_component_select_expression_set_expression(
            'dynamic_handler', source_expression)

    def set_spanner(self, source_expression):
        r'''Set spanner to `source_expression`.

        Return spanner set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, spannertools.Spanner), repr(source_expression)
        assert not len(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        return self._store_counttime_component_select_expression_set_expression(
            'spanner', source_expression)
