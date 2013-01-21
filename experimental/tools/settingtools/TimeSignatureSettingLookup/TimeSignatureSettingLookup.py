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
        # ignore voice_name input parameter
        voice_name = None
        segment_specification = score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        # TODO: eventually change to result = self._apply_callbacks(time_signatures)
        time_signatures, dummy = self._apply_callbacks(time_signatures, None)
        # TODO: eventually return TimeSignatureRegionProduct instead of tuple of time signatures
        return time_signatures
