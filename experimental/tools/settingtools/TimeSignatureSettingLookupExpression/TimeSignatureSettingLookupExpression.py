from experimental.tools.settingtools.SettingLookupExpression import SettingLookupExpression


class TimeSignatureSettingLookupExpression(SettingLookupExpression):
    '''Time signature setting lookup.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookupExpression.__init__(self, attribute='time_signatures', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        segment_specification = self.score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        # TODO: maybe use PayloadExpression here instead to avoid dummy start positioning?
        # TODO: use start_offset of segment_specification?
        result = settingtools.StartPositionedDivisionPayloadExpression(
            time_signatures, start_offset=0, voice_name='dummy voice name')
        result = self._apply_callbacks(result)
        # TODO: eventually return TimeSignatureRegionProduct instead of tuple of time signatures
        time_signatures = result.payload
        return time_signatures
