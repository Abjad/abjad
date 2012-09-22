from experimental.settingtools.Command import Command


class RhythmCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a rhythm payload will apply.
    '''
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'rhythm'
