from experimental.tools.requesttools.CommandRequest import CommandRequest


class DivisionCommandRequest(CommandRequest):
    '''Division command request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, request_modifiers=None):
        CommandRequest.__init__(self, 'divisions', voice_name, offset,
            request_modifiers=request_modifiers)
