import copy
from experimental.tools.expressiontools.InputSetExpression import InputSetExpression


class MultipleContextSetExpression(InputSetExpression):
    r'''Multiple-context set expression.

    Set `attribute` to `source` for `anchor` target timespan over all `contexts`:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> z(multiple_context_set_expression)
        expressiontools.MultipleContextSetExpression(
            attribute='time_signatures',
            source=expressiontools.PayloadExpression(
                ((4, 8), (3, 8))
                ),
            anchor='red',
            persist=True
            )

    Composers create multiple-context set expressions with set methods.
    '''

    ### INITIAILIZER ###

    def __init__(self, attribute=None, source=None, anchor=None, context_names=None, 
            persist=True, truncate=None):
        InputSetExpression.__init__(self, attribute=attribute, source=source, anchor=anchor, 
            persist=persist, truncate=truncate)
        assert isinstance(context_names, (list, type(None))), repr(context_names)
        self._context_names = context_names

    ### PRIVATE METHODS ###
    
    def _attribute_to_single_context_set_expression_class(self, attribute):
        from experimental.tools import expressiontools
        return {
            'time_signatures': expressiontools.SingleContextTimeSignatureSetExpression,
            'divisions': expressiontools.SingleContextDivisionSetExpression,
            'rhythm': expressiontools.SingleContextRhythmSetExpression,
            }[attribute]
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        '''Multiple-context set expression context names.
    
        Return list of strings or none.
        '''
        return self._context_names

    ### PUBLIC METHODS ###

    def evaluate(self):
        single_context_set_expressions = []
        single_context_set_expression_class = \
            self._attribute_to_single_context_set_expression_class(self.attribute)
        if self.context_names is None:
            anchor = copy.deepcopy(self.anchor)
            single_context_set_expression = single_context_set_expression_class(
                self.source, 
                anchor,
                context_name=None,
                persist=self.persist)
            single_context_set_expression._score_specification = self.score_specification
            single_context_set_expressions.append(single_context_set_expression)
        else:
            for context_name in self.context_names:
                anchor = copy.deepcopy(self.anchor)
                single_context_set_expression = single_context_set_expression_class(
                    self.source, 
                    anchor,
                    context_name=context_name,
                    persist=self.persist)
                single_context_set_expression._score_specification = self.score_specification
                single_context_set_expressions.append(single_context_set_expression)
        if self.attribute == 'divisions':
            for single_context_set_expression in single_context_set_expressions:
                single_context_set_expression._truncate = self.truncate
        return single_context_set_expressions
