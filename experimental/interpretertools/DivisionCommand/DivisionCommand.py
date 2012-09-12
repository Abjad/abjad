from experimental.interpretertools.Command import Command


class DivisionCommand(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a division payload will apply.
    '''

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'divisions'
