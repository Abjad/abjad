from abjad.tools import durationtools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.SelectExpression import SelectExpression


class DivisionSelectExpression(SelectExpression):
    r'''Division select expression:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` divisions that start during score::

        >>> select_expression = score_specification.interface.select_divisions('Voice 1')

    ::
        
        >>> z(select_expression)
        settingtools.DivisionSelectExpression(
            voice_name='Voice 1'
            )

    Select voice ``1`` divisions that start during segment ``'red'``::

        >>> select_expression = red_segment.select_divisions('Voice 1')

    ::

        >>> z(select_expression)
        settingtools.DivisionSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Division select expressions are immutable.
    '''
    
    ### PRIVATE METHODS ###

    def _get_divisions_that_satisfy_time_relation(self, divisions, time_relation):
        result = []
        for division in divisions:
            if time_relation(
                timespan_2=division, 
                score_specification=self.score_specification, 
                context_name=self.voice_name):
                result.append(division)
        return result

    def _get_time_relation(self, anchor_timespan):
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        else:
            time_relation = self.time_relation.new(timespan_1=anchor_timespan)
        return time_relation
        
    def _evaluate(self):
        from experimental.tools import settingtools
        anchor_timespan = self.get_anchor_timespan()
        voice_proxy = self.score_specification.contexts[self.voice_name]
        division_products = voice_proxy.division_products
        if division_products is None:
            return
        existing_voice_divisions = []
        for division_product in division_products:
            existing_voice_divisions.extend(division_product.payload.divisions)
        time_relation = self._get_time_relation(anchor_timespan)
        divisions = self._get_divisions_that_satisfy_time_relation(existing_voice_divisions, time_relation)
        if not divisions:
            return None
        start_offset = divisions[0].start_offset
        expression = settingtools.StartPositionedDivisionPayloadExpression(divisions, start_offset=start_offset)
        if self.time_relation is None:
            inventory = expression & anchor_timespan
            expression = inventory[0]
        expression = self._apply_callbacks(expression)
        expression._voice_name = self.voice_name 
        return expression
