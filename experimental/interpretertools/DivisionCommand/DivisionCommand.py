from experimental.interpretertools.Command import Command


class DivisionCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time 
    to which an evaluated request will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, request, start_segment_identifier, context_name,
        segment_start_offset, segment_stop_offset, duration, fresh=None, truncate=None):
        Command.__init__(self, request, start_segment_identifier, context_name,
            segment_start_offset, segment_stop_offset, duration, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'divisions'

    @property
    def truncate(self):
        '''Not yet implemented.
        '''
        return self._truncate
