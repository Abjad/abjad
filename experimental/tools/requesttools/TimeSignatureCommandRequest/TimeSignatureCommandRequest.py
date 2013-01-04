from experimental.tools.requesttools.CommandRequest import CommandRequest


class TimeSignatureCommandRequest(CommandRequest):
    '''Time signature command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, request_modifiers=None):
        CommandRequest.__init__(self, 'time_signatures', voice_name, offset,
            request_modifiers=request_modifiers)

    ### PUBLIC METHODS ###

    def _get_payload(self, score_specification, voice_name=None):
        segment_specification = score_specification.get_start_segment_specification(self.offset)
        time_signatures = segment_specification.time_signatures[:]
        time_signatures, dummy = self._apply_request_modifiers(time_signatures, None)
        return time_signatures
