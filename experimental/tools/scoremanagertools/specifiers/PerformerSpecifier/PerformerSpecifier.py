from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class PerformerSpecifier(ParameterSpecifier):

    def __init__(self, description=None, name=None, performer=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.performer = performer

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        if self.name:
            return self.name
        elif self.performer:
            return self.performer.name
