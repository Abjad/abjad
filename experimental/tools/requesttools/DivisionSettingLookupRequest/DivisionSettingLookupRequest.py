from experimental.tools import timerelationtools
from experimental.tools import timespantools
from experimental.tools.requesttools.SettingLookupRequest import SettingLookupRequest


class DivisionSettingLookupRequest(SettingLookupRequest):
    '''Division setting lookup request.

    Example. Look up division setting active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> measure = red_segment.select_background_measures('Voice 1')[4:5]
        >>> setting = measure.start_offset.look_up_division_setting('Voice 1')

    ::

        >>> z(setting)
        requesttools.DivisionSettingLookupRequest(
            'Voice 1',
            settingtools.OffsetExpression(
                anchor=selectortools.BackgroundMeasureSelector(
                    anchor='red',
                    voice_name='Voice 1',
                    payload_callbacks=settingtools.CallbackInventory([
                        'result = self.___getitem__(elements, start_offset, slice(4, 5, None))'
                        ])
                    )
                )
            )

    Composers create division setting lookup requests during specification time.

    Composers create division setting lookup requests through a method
    implemented on ``OffsetExpression``.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, payload_callbacks=None):
        SettingLookupRequest.__init__(self, 'divisions', voice_name, offset,
            payload_callbacks=payload_callbacks)

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name):
        from experimental.tools import settingtools
        requested_segment_identifier = self.offset.start_segment_identifier
        requested_offset = self.offset._get_offset(score_specification, voice_name)
        timespan_inventory = timespantools.TimespanInventory()
        for division_region_command in score_specification.division_region_commands:
            if not division_region_command.request == self:
                timespan_inventory.append(division_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = score_specification.get_start_segment_specification(requested_segment_identifier)
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        absolute_request = source_command.request
        assert isinstance(absolute_request, settingtools.AbsoluteExpression), repr(absolute_request)
        divisions = absolute_request.payload
        start_offset = division_region_command.timespan.start_offset
        divisions, start_offset = self._apply_payload_callbacks(divisions, start_offset)
        return divisions
