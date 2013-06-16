from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class TempoSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.name
