from experimental.tools.requesttools.SettingLookupRequest import SettingLookupRequest


class TimeSignatureSettingLookupRequest(SettingLookupRequest):
    '''Time signature command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, payload_callbacks=None):
        SettingLookupRequest.__init__(self, 'time_signatures', voice_name, offset,
            payload_callbacks=payload_callbacks)

    ### PUBLIC METHODS ###

    def _get_payload(self, score_specification, voice_name=None):
        segment_specification = score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures, dummy = self._apply_payload_callbacks(time_signatures, None)
        return time_signatures
