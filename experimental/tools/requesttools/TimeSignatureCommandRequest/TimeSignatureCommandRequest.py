from experimental.tools.requesttools.CommandRequest import CommandRequest


class TimeSignatureCommandRequest(CommandRequest):
    '''Time signature command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, request_modifiers=None):
        CommandRequest.__init__(self, 'time_signatures', voice_name, offset,
            request_modifiers=request_modifiers)
