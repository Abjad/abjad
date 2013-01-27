from experimental.tools import timerelationtools
from experimental.tools import timespantools
from experimental.tools.expressiontools.SettingLookupExpression import SettingLookupExpression


class SetDivisionLookupExpression(SettingLookupExpression):
    '''Division setting lookup.

    Example. Look up set-division expression active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measure = red_segment.select_measures('Voice 1')[4:5]
        >>> setting = measure.start_offset.look_up_division_setting('Voice 1')

    ::

        >>> z(setting)
        expressiontools.SetDivisionLookupExpression(
            voice_name='Voice 1',
            offset=expressiontools.OffsetExpression(
                anchor=expressiontools.MeasureSelectExpression(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=expressiontools.CallbackInventory([
                        'result = self.___getitem__(payload_expression, slice(4, 5, None))'
                        ])
                    )
                )
            )

    Composers create set-division lookup expressions during specification time.

    Composers create set-division lookup expressions through a method
    implemented on ``OffsetExpression``.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookupExpression.__init__(self, attribute='divisions', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _get_timespan_scoped_single_context_division_settings(self):
        result = timespantools.TimespanInventory()
        for timespan_scoped_single_context_division_setting in self.score_specification.timespan_scoped_single_context_division_settings:
            if not timespan_scoped_single_context_division_setting.expression == self:
                result.append(timespan_scoped_single_context_division_setting)
        return result

    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        start_segment_identifier = self.offset.start_segment_identifier
        expression = self.offset.evaluate()
        offset = expression.payload[0]
        timespan_inventory = self._get_timespan_scoped_single_context_division_settings()
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = self.score_specification.get_start_segment_specification(start_segment_identifier)
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        expression = source_command.expression
        assert isinstance(expression, expressiontools.PayloadExpression), repr(expression)
        expression = self._apply_callbacks(expression)
        return expression
