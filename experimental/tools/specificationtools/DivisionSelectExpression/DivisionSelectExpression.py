from abjad.tools import durationtools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.specificationtools.SelectExpression import SelectExpression


class DivisionSelectExpression(SelectExpression):
    r'''Division select expression.

    Definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example 1. Select voice ``1`` divisions that start during score:

    ::

        >>> select_expression = score_specification.select_divisions('Voice 1')

    ::

        >>> z(select_expression)
        specificationtools.DivisionSelectExpression(
            voice_name='Voice 1'
            )

    Example 2. Select voice ``1`` divisions that start during segment ``'red'``:

    ::

        >>> select_expression = red_segment.select_divisions('Voice 1')

    ::

        >>> z(select_expression)
        specificationtools.DivisionSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Division select expressions are immutable.
    '''

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate division select expression.

        Return none when nonevaluable.

        Return start-positioned division payload expression when evaluable.
        '''
        from experimental.tools import specificationtools
        anchor_timespan = self._evaluate_anchor_timespan()
        time_relation = self._get_time_relation(anchor_timespan)
        voice_proxy = self.score_specification.payload_expressions_by_voice[self.voice_name]
        division_payload_expressions = voice_proxy.payload_expressions_by_attribute['divisions']
        if division_payload_expressions is None:
            return
        existing_voice_divisions = []
        for division_payload_expression in division_payload_expressions:
            existing_voice_divisions.extend(division_payload_expression.payload.divisions)
        if not existing_voice_divisions:
            return
        start_offset = existing_voice_divisions[0].start_offset
        expression = specificationtools.StartPositionedDivisionPayloadExpression(
            existing_voice_divisions, start_offset=start_offset)
        expression = expression.get_elements_that_satisfy_time_relation(time_relation)
        if self.time_relation is None:
            inventory = expression & anchor_timespan
            expression = inventory[0]
        result = self._apply_callbacks(expression)
        if isinstance(result, list):
            expressions = []
            for expression in result:
                expression._voice_name = self.voice_name
                expressions.append(expression)
            return expressions
        else: 
            expression = result
            expression._voice_name = self.voice_name
            return expression
