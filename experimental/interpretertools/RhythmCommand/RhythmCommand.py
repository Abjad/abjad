from experimental.interpretertools.Command import Command


class RhythmCommand(Command):
    r'''.. versionadded:: 1.0

    Rhythm command created during interpretation.
    '''
    
    ### INITIALIZER ###

    def __init__(self, value, fresh):
        self._value = value
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def fresh(self):
        return self._fresh

    @property
    def value(self):
        return self._value
