from experimental.tools.settingtools.SettingLookup import SettingLookup


class TimeSignatureSettingLookup(SettingLookup):
    '''Time signature setting lookup.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookup.__init__(self, attribute='time_signatures', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def _evaluate(self, score_specification, voice_name=None):
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        segment_specification = score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        result = settingtools.MeasureRegionProduct(
            time_signatures, voice_name='dummy voice name', start_offset=0)
        # TODO: eventually change to result = self._apply_callbacks(time_signatures)
        result, dummy = self._apply_callbacks(result, None)
        # TODO: eventually return TimeSignatureRegionProduct instead of tuple of time signatures
        time_signatures = result.payload
        return time_signatures
