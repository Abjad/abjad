from experimental.interpretertools.Command import Command


class RhythmCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a rhythm-maker will apply.
    '''
    
    ### INITIALIZER ###

    def __init__(self, value, duration, start_offset, stop_offset, context_name, fresh):
        Command.__init__(self, value, duration, start_offset, stop_offset, context_name)
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def fresh(self):
        return self._fresh
