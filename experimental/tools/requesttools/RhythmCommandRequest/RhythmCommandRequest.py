from experimental.tools.requesttools.CommandRequest import CommandRequest


class RhythmCommandRequest(CommandRequest):
    '''Rhythm command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, request_modifiers=None):
        CommandRequest.__init__(self, 'rhythm', voice_name, offset,
            request_modifiers=request_modifiers)
