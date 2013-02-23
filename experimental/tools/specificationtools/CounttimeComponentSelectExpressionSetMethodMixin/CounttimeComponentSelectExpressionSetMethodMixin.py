from abjad.tools import spannertools
from abjad.tools.abctools import AbjadObject


class CounttimeComponentSelectExpressionSetMethodMixin(AbjadObject):
    '''Counttime component set method mixin.
    '''

    ### PRIVATE METHODS ###

    def _attribute_to_set_expression_class(self, attribute):
        from experimental.tools import specificationtools
        return {
            'spanner': specificationtools.SpannerSetExpression,
            }[attribute]

    def _store_counttime_component_select_expression_set_expression(self, attribute, source_expression):
        from experimental.tools import specificationtools
        set_expression_class = self._attribute_to_set_expression_class(attribute)
        source_expression = self._expr_to_expression(source_expression)
        target_counttime_component_select_expression = self
        counttime_component_select_expression_set_expression = set_expression_class(
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory
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

    def set_spanner(self, source_expression):
        r'''Set spanner to `source_expression`.

        Return spanner set expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(source_expression, spannertools.Spanner), repr(source_expression)
        source_expression = specificationtools.PayloadExpression(payload=source_expression)
        return self._store_counttime_component_select_expression_set_expression(
            'spanner', source_expression)
