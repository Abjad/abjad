import copy
from experimental.tools.specificationtools.TimeContiguousAnchoredSetExpression import TimeContiguousAnchoredSetExpression


class MultipleContextSetExpression(TimeContiguousAnchoredSetExpression):
    r'''Multiple-context set expression.

    Set `attribute` to `source_expression` for `target_timespan` over all `contexts`:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> z(multiple_context_set_expression)
        specificationtools.MultipleContextSetExpression(
            attribute='time_signatures',
            source_expression=specificationtools.IterablePayloadExpression(
                payload=((4, 8), (3, 8))
                ),
            target_timespan='red',
            persist=True
            )

    Set methods create multiple-context set expressions.
    '''

    ### INITIAILIZER ###

    def __init__(self, 
            attribute=None, source_expression=None, target_timespan=None, target_context_names=None, 
            persist=True, truncate=None):
        TimeContiguousAnchoredSetExpression.__init__(self, attribute=attribute, 
            source_expression=source_expression, 
            target_timespan=target_timespan, persist=persist, truncate=truncate)
        assert isinstance(target_context_names, (list, type(None))), repr(target_context_names)
        self._target_context_names = target_context_names

    ### PRIVATE METHODS ###
    
    def _attribute_to_single_context_set_expression_class(self, attribute):
        from experimental.tools import specificationtools
        return {
            'time_signatures': specificationtools.SingleContextTimeSignatureSetExpression,
            'divisions': specificationtools.SingleContextDivisionSetExpression,
            'rhythm': specificationtools.SingleContextRhythmSetExpression,
            }[attribute]
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def target_context_names(self):
        '''Multiple-context set expression target context names.
    
        Return list or none.
        '''
        return self._target_context_names

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate multiple-context set expression.

        Return list of single-context set expressions.
        '''
        single_context_set_expressions = []
        single_context_set_expression_class = \
            self._attribute_to_single_context_set_expression_class(self.attribute)
        if self.target_context_names is None:
            target_context_names = [None]
        else:
            target_context_names = self.target_context_names
        for target_context_name in target_context_names:
            target_timespan = copy.deepcopy(self.target_timespan)
            single_context_set_expression = single_context_set_expression_class(
                source_expression=self.source_expression, 
                target_timespan=target_timespan,
                target_context_name=target_context_name,
                persist=self.persist)
            single_context_set_expression._score_specification = self.score_specification
            single_context_set_expression._lexical_rank = self._lexical_rank
            single_context_set_expressions.append(single_context_set_expression)
        if self.attribute == 'divisions':
            for single_context_set_expression in single_context_set_expressions:
                single_context_set_expression._truncate = self.truncate
        return single_context_set_expressions

    def evaluate_and_store_in_root_specification(self):
        '''Evaluate multiple-context set expression and store in root specification.

        Return none.
        ''' 
        fresh_single_context_set_expressions = self.evaluate()
        assert all([x.fresh for x in fresh_single_context_set_expressions])
        self.root_specification.fresh_single_context_set_expressions.extend(
            fresh_single_context_set_expressions)
