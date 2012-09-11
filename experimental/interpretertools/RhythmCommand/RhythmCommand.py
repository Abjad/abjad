from experimental.interpretertools.Command import Command


class RhythmCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a rhythm-maker will apply.
    '''
    
    ### INITIALIZER ###

    def __init__(self, resolved_value, segment_identifier, context_name, 
        segment_start_offset, segment_stop_offset, duration, fresh):
        Command.__init__(self, resolved_value, segment_identifier, context_name, 
            segment_start_offset, segment_stop_offset, duration)
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def fresh(self):
        return self._fresh
