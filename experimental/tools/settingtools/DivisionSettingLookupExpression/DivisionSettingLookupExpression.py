from experimental.tools import timerelationtools
from experimental.tools import timespantools
from experimental.tools.settingtools.SettingLookupExpression import SettingLookupExpression


class DivisionSettingLookupExpression(SettingLookupExpression):
    '''Division setting lookup.

    Example. Look up division setting active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measure = red_segment.select_measures('Voice 1')[4:5]
        >>> setting = measure.start_offset.look_up_division_setting('Voice 1')

    ::

        >>> z(setting)
        settingtools.DivisionSettingLookupExpression(
            voice_name='Voice 1',
            offset=settingtools.OffsetExpression(
                anchor=selectortools.MeasureSelector(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=settingtools.CallbackInventory([
                        'result = self.___getitem__(payload_expression, slice(4, 5, None))'
                        ])
                    )
                )
            )

    Composers create division setting lookups during specification time.

    Composers create division setting lookups through a method
    implemented on ``OffsetExpression``.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookupExpression.__init__(self, attribute='divisions', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        start_segment_identifier = self.offset.start_segment_identifier
        offset = self.offset._evaluate()
        timespan_inventory = timespantools.TimespanInventory()
        for division_region_command in self.score_specification.division_region_commands:
            if not division_region_command.expression == self:
                timespan_inventory.append(division_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = self.score_specification.get_start_segment_specification(start_segment_identifier)
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        expression = source_command.expression
        assert isinstance(expression, settingtools.PayloadExpression), repr(expression)
        result = self._apply_callbacks(expression)
        # TODO: eventually return PayloadExpression instead of tuple of divisions
        return result.payload
