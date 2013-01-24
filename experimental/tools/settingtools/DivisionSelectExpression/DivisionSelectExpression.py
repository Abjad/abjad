from abjad.tools import durationtools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.SelectExpression import SelectExpression


class DivisionSelectExpression(SelectExpression):
    r'''Division selector:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` divisions that start during score::

        >>> selector = score_specification.interface.select_divisions('Voice 1')

    ::
        
        >>> z(selector)
        settingtools.DivisionSelectExpression(
            voice_name='Voice 1'
            )

    Select voice ``1`` divisions that start during segment ``'red'``::

        >>> selector = red_segment.select_divisions('Voice 1')

    ::

        >>> z(selector)
        settingtools.DivisionSelectExpression(
            anchor='red',
            voice_name='Voice 1'
            )

    Division selectors are immutable.
    '''
    
    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        anchor_timespan = self.get_anchor_timespan()
        voice_proxy = self.score_specification.contexts[self.voice_name]
        division_products = voice_proxy.division_products
        if division_products is None:
            return None
        existing_voice_divisions = []
        for division_product in division_products:
            existing_voice_divisions.extend(division_product.payload.divisions)
        timespan_1 = anchor_timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        else:
            time_relation = self.time_relation.new(timespan_1=anchor_timespan)
        divisions = []
        for division in existing_voice_divisions:
            if time_relation(timespan_2=division, 
                score_specification=self.score_specification, 
                context_name=self.voice_name):
                divisions.append(division)
        if not divisions:
            return None
        start_offset = divisions[0].start_offset
        result = settingtools.StartPositionedDivisionPayloadExpression(
            divisions, voice_name=self.voice_name, start_offset=start_offset)
        if self.time_relation is None:
            result &= anchor_timespan
            result = result[0]
        result = self._apply_callbacks(result)
        assert isinstance(result, settingtools.StartPositionedDivisionPayloadExpression), repr(result)
        return result
